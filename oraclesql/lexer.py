from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name, Punctuation, Text, Whitespace, Comment

# Import all builtins, including new system object and refined lists
from oraclesql._oraclesql_builtins import (
    ORACLE_KEYWORDS_MAIN_CONTROL,
    ORACLE_KEYWORDS_AUXILIARY,
    ORACLE_KEYWORDS_PLSQL,
    ORACLE_KEYWORDS_TYPE,
    ORACLE_BUILTINS_NAME,
    ORACLE_SYS_PCK_PREF,
    ORACLE_SYS_OBJ_PREF
)

# Create combined sets for efficient lookup
ALL_PLSQL_KEYWORDS = set(ORACLE_KEYWORDS_PLSQL)
ALL_MAIN_CONTROL_KEYWORDS = set(ORACLE_KEYWORDS_MAIN_CONTROL)
ALL_AUXILIARY_KEYWORDS = set(ORACLE_KEYWORDS_AUXILIARY)
ALL_TYPES = set(ORACLE_KEYWORDS_TYPE)
ALL_BUILTINS = set(ORACLE_BUILTINS_NAME)

# Convert prefixes to tuples for fast string matching
PACKAGE_PREFIXES_TUPLE = tuple(ORACLE_SYS_PCK_PREF)
SYSTEM_OBJECT_PREFIXES_TUPLE = tuple(ORACLE_SYS_OBJ_PREF)

__all__ = ["OracleSQLLexer"]

class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql","ora","plsql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        
        # Mappings for token refinement: (word set, specific token type)
        KEYWORD_MAPPINGS = [
            (ALL_MAIN_CONTROL_KEYWORDS, Keyword.Control),       # SELECT, FROM, WHERE, CREATE, etc.
            (ALL_PLSQL_KEYWORDS, Keyword.Declaration),           # BEGIN, IF, LOOP, etc.
            (ALL_AUXILIARY_KEYWORDS, Keyword.Constant),          # AND, LIKE, ON, BETWEEN, etc.
            (ALL_TYPES, Keyword.Type),                          # VARCHAR2, NUMBER, etc.
            (ALL_BUILTINS, Name.Builtin),                       # COUNT, TO_DATE, ROWNUM, etc.
        ]

        # 0=none, 1=package_name_seen, 2=dot_seen_expecting_method
        package_chain_state = 0
        package_chain_buffer = [] # Buffer for (index, token, value) of the package.function chain

        # Helper function to yield the buffered chain as a single token
        # FIX: Ensure correct token type and handle empty buffer gracefully
        def flush_and_yield_buffer(final_token=None):
            nonlocal package_chain_state, package_chain_buffer
            
            if not package_chain_buffer:
                return # Exit if buffer is empty
            
            # The token to yield: use final_token, or the token of the first item (Name/Keyword)
            token_to_yield = final_token if final_token else package_chain_buffer[0][1]
            start_index = package_chain_buffer[0][0]
            
            # Combine all parts of the buffer (including whitespace and dot)
            full_value = "".join(item[2] for item in package_chain_buffer)
            
            yield start_index, token_to_yield, full_value
            
            package_chain_buffer = []
            package_chain_state = 0

        # Use parent lexer for initial tokenization
        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            
            # Non-code tokens (yield and maintain buffer if in chain)
            if token in Comment or token is Text or token is Whitespace:
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
                    yield from flush_and_yield_buffer(Name.Namespace)
                    continue

                # B. Check for SYSTEM PACKAGE prefixes (DBMS_..., UTL_...) - START OF CHAIN
                if val_upper.startswith(PACKAGE_PREFIXES_TUPLE):
                    # Flush any unexpected/incomplete chain, then start new chain
                    yield from flush_and_yield_buffer() 
                    package_chain_buffer.append((index, token, value))
                    package_chain_state = 1 # Mark: we saw a package name
                    continue
                
                # C. Check for SYSTEM OBJECT prefixes (DBA_HIST_..., V$...) - NO CHAIN
                if val_upper.startswith(SYSTEM_OBJECT_PREFIXES_TUPLE):
                    yield from flush_and_yield_buffer() # Flush any incomplete chain
                    yield index, Name.Namespace, value # Highlight as a distinct system object
                    continue
                
                # D. Refine regular tokens (Keywords, Types, Builtins) - NO CHAIN
                found_match = False
                for word_set, token_type in KEYWORD_MAPPINGS:
                    if val_upper in word_set:
                        yield from flush_and_yield_buffer() # Flush any incomplete chain
                        yield index, token_type, value
                        found_match = True
                        break
                
                if found_match:
                    continue

                # E. Plain identifier (user table, column, variable)
                yield from flush_and_yield_buffer() # Flush any incomplete chain
                yield index, token, value

            elif token is Punctuation and value == '.':
                # Dot in chain
                if package_chain_state == 1:
                    package_chain_buffer.append((index, token, value)) # Save the dot
                    package_chain_state = 2 # Package seen, expect method next
                else:
                    # Not in a package chain (e.g., table.column)
                    yield from flush_and_yield_buffer()
                    yield index, token, value
            
            else:
                # Any other token (e.g., Literal, Operator) breaks the chain
                yield from flush_and_yield_buffer()
                yield index, token, value
        
        # Flush anything left in the buffer at the end of the text
        yield from flush_and_yield_buffer()



