from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name, Punctuation, Text, Whitespace, Comment

# Import new, optimized lists
from oraclesql._oraclesql_builtins import (
    ORACLE_KEYWORDS_MAIN_CONTROL,
    ORACLE_KEYWORDS_AUXILIARY,
    ORACLE_KEYWORDS_PLSQL,
    ORACLE_KEYWORDS_TYPE,
    ORACLE_BUILTINS_NAME,
    ORACLE_SYS_PCK_PREF
)

# Create combined sets for efficient lookup
ALL_PLSQL_KEYWORDS = set(ORACLE_KEYWORDS_PLSQL)
ALL_MAIN_CONTROL_KEYWORDS = set(ORACLE_KEYWORDS_MAIN_CONTROL)
ALL_AUXILIARY_KEYWORDS = set(ORACLE_KEYWORDS_AUXILIARY)
ALL_TYPES = set(ORACLE_KEYWORDS_TYPE)
ALL_BUILTINS = set(ORACLE_BUILTINS_NAME)

# Convert package prefixes to tuple for fast string matching
PACKAGE_PREFIXES_TUPLE = tuple(ORACLE_SYS_PCK_PREF)

__all__ = ["OracleSQLLexer"]

class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        
        # Mappings for token refinement: (word set, specific token type)
        # Order is important for lookup speed
        KEYWORD_MAPPINGS = [
            (ALL_MAIN_CONTROL_KEYWORDS, Keyword.Control),        # SELECT, FROM, WHERE, CREATE, etc.
            (ALL_PLSQL_KEYWORDS, Keyword.Declaration),           # BEGIN, IF, LOOP, etc.
            (ALL_AUXILIARY_KEYWORDS, Keyword.Constant),          # AND, LIKE, ON, BETWEEN, etc.
            (ALL_TYPES, Keyword.Type),                           # VARCHAR2, NUMBER, etc.
            (ALL_BUILTINS, Name.Builtin),                        # COUNT, TO_DATE, ROWNUM, etc.
        ]

        # 0=none, 1=package_name_seen, 2=dot_seen_expecting_method
        package_chain_state = 0

        # Use parent lexer for initial tokenization
        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            
            # Skip non-code tokens, continue package chain state
            if token in Comment or token is Text or token is Whitespace:
                yield index, token, value
                continue
            
            val_upper = value.upper()

            # Process identifiers, keywords, and built-ins
            if token in (Name, Name.Builtin, Keyword):
                
                # A. Handle method after dot (DBMS_OUTPUT.PUT_LINE)
                if package_chain_state == 2:
                    yield index, Name.Function, value
                    package_chain_state = 0
                    continue

                # B. Check for package prefixes (DBMS_..., UTL_...)
                if val_upper.startswith(PACKAGE_PREFIXES_TUPLE):
                    yield index, Name.Namespace, value
                    package_chain_state = 1 
                    continue
                
                # C. Refine token type returned by SqlLexer
                found_match = False
                for word_set, token_type in KEYWORD_MAPPINGS:
                    if val_upper in word_set:
                        # Replace general token (Keyword/Name) with specific one
                        yield index, token_type, value
                        found_match = True
                        break
                
                if found_match:
                    package_chain_state = 0
                    continue

                # D. Plain identifier or keyword returned by parent that we didn't refine
                package_chain_state = 0
                yield index, token, value

            elif token is Punctuation and value == '.':
                # Update chain state for dots
                if package_chain_state == 1:
                    package_chain_state = 2 # Package seen, expect method next
                else:
                    package_chain_state = 0
                yield index, token, value
            
            else:
                # Any other token (e.g., Literal, Operator) breaks the chain
                package_chain_state = 0
                yield index, token, value

