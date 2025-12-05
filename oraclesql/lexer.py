from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name, Punctuation, Text, Whitespace, Comment

# Import lists
from oraclesql._oraclesql_builtins import (
    ORACLE_KEYWORDS_MAIN_CONTROL,
    ORACLE_KEYWORDS_AUXILIARY,
    ORACLE_KEYWORDS_PLSQL,
    ORACLE_KEYWORDS_TYPE,
    ORACLE_BUILTINS_NAME,
    ORACLE_SYS_PCK_PREF,
    ORACLE_SYS_OBJ_PREF # System Objects still needed for DBA_ etc.
)

# Create combined sets for efficient lookup
ALL_PLSQL_KEYWORDS = set(ORACLE_KEYWORDS_PLSQL)
ALL_MAIN_CONTROL_KEYWORDS = set(ORACLE_KEYWORDS_MAIN_CONTROL)
ALL_AUXILIARY_KEYWORDS = set(ORACLE_KEYWORDS_AUXILIARY)
ALL_TYPES = set(ORACLE_KEYWORDS_TYPE)
ALL_BUILTINS = set(ORACLE_BUILTINS_NAME)
PACKAGE_PREFIXES_TUPLE = tuple(ORACLE_SYS_PCK_PREF)
SYSTEM_OBJECT_PREFIXES_TUPLE = tuple(ORACLE_SYS_OBJ_PREF)

__all__ = ["OracleSQLLexer"]

class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        
        KEYWORD_MAPPINGS = [
            (ALL_MAIN_CONTROL_KEYWORDS, Keyword.Control),   
            (ALL_PLSQL_KEYWORDS, Keyword.Declaration),       
            (ALL_AUXILIARY_KEYWORDS, Keyword.Constant),      
            (ALL_TYPES, Keyword.Type),                      
            (ALL_BUILTINS, Name.Builtin),                   
        ]

        # 0=none, 1=package_name_seen, 2=dot_seen_expecting_method
        package_chain_state = 0
        package_chain_buffer = [] # Buffer to store index, token, value of the chain (e.g., dbms_output)

        # Use parent lexer for initial tokenization
        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            
            # Helper to flush buffer and reset state
            def flush_and_yield_buffer(final_token=None):
                nonlocal package_chain_state, package_chain_buffer
                # If we have a buffer, yield it
                if package_chain_buffer:
                    # Yield the whole chain as one token at the starting index
                    start_index = package_chain_buffer[0][0]
                    full_value = "".join(item[2] for item in package_chain_buffer)
                    
                    # Use the final_token provided, or Name.Builtin as default for the system call
                    yield start_index, final_token if final_token else Name.Builtin, full_value
                
                # Reset
                package_chain_buffer = []
                package_chain_state = 0

            # --- Start Logic ---
            
            # Non-code tokens (yield and maintain buffer if not broken)
            if token in Comment or token is Text or token is Whitespace:
                # If we are in chain state, append it to buffer (e.g. whitespace between tokens)
                if package_chain_state > 0:
                    package_chain_buffer.append((index, token, value))
                else:
                    yield index, token, value
                continue
            
            val_upper = value.upper()

            # Process Identifiers, Keywords, and Built-ins
            if token in (Name, Name.Builtin, Keyword):
                
                # A. Handle method after dot (State 2) - END OF CHAIN
                if package_chain_state == 2:
                    # Final part of the chain (the function name)
                    package_chain_buffer.append((index, token, value))
                    # FLUSH: Yield the whole package.function as a single Name.Builtin token
                    yield from flush_and_yield_buffer(Name.Builtin)
                    continue

                # B. Check for SYSTEM PACKAGE prefixes (DBMS_..., UTL_...) - START OF CHAIN
                if val_upper.startswith(PACKAGE_PREFIXES_TUPLE):
                    # Save the package name to buffer, do NOT yield yet
                    package_chain_buffer.append((index, token, value))
                    package_chain_state = 1 # Mark: we saw a package name
                    continue
                
                # C. Check for SYSTEM OBJECT prefixes (DBA_HIST_..., V$...) - NO CHAIN
                if val_upper.startswith(SYSTEM_OBJECT_PREFIXES_TUPLE):
                    # Flush any incomplete chain, then yield current token as Name.Label
                    yield from flush_and_yield_buffer() 
                    yield index, Name.Label, value
                    continue
                
                # D. Refine regular tokens (Keywords, Types, Builtins) - NO CHAIN
                found_match = False
                for word_set, token_type in KEYWORD_MAPPINGS:
                    if val_upper in word_set:
                        # Flush any incomplete chain, then yield current token
                        yield from flush_and_yield_buffer()
                        yield index, token_type, value
                        found_match = True
                        break
                
                if found_match:
                    continue

                # E. Plain identifier (user table, column, variable)
                # Flush any incomplete chain, then yield current token
                yield from flush_and_yield_buffer() 
                yield index, token, value

            elif token is Punctuation and value == '.':
                # Dot in chain
                if package_chain_state == 1:
                    package_chain_buffer.append((index, token, value)) # Save the dot
                    package_chain_state = 2 # Package seen, expect method next
                else:
                    # Flush any incomplete chain (e.g. table.column), then yield the dot
                    yield from flush_and_yield_buffer()
                    yield index, token, value
            
            else:
                # Any other token (e.g., Literal, Operator) breaks the chain
                yield from flush_and_yield_buffer()
                yield index, token, value
        
        # Flush anything left in the buffer at the end of the text
        yield from flush_and_yield_buffer()
