from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name, Punctuation, Text, Whitespace, Comment

# 1. Импортируем новые, оптимизированные списки
from oraclesql._oraclesql_builtins import (
    ORACLE_KEYWORDS_CONTROL,
    ORACLE_KEYWORDS_PLSQL,
    ORACLE_KEYWORDS_TYPE,
    ORACLE_BUILTINS_NAME,
    ORACLE_SYS_PCK_PREF
)

# 2. Создаем объединенные наборы для эффективной проверки
# Все управляющие ключевые слова (SQL + PL/SQL)
ALL_CONTROL_KEYWORDS = set(ORACLE_KEYWORDS_CONTROL + ORACLE_KEYWORDS_PLSQL)
# Все типы данных
ALL_TYPES = set(ORACLE_KEYWORDS_TYPE)
# Все встроенные функции/псевдо-колонки
ALL_BUILTINS = set(ORACLE_BUILTINS_NAME)

# Превращаем список префиксов в кортеж (tuple) для быстрой проверки startswith()
PACKAGE_PREFIXES_TUPLE = tuple(ORACLE_SYS_PCK_PREF)

__all__ = ["OracleSQLLexer"]

class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        # Структура для проверки: (набор слов, тип токена)
        extra_content = [
            (ALL_TYPES, Name.Builtin),      # Выделяем типы данных как встроенные имена
            (ALL_BUILTINS, Name.Builtin),   # Выделяем встроенные функции/псевдо-колонки как встроенные имена
            (ALL_CONTROL_KEYWORDS, Keyword.Control) # Выделяем управляющие слова (SQL/PLSQL) как ключевые слова
        ]

        # 0=ничего, 1=пакет, 2=точка (ждем метод)
        package_chain_state = 0

        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            # Skip spaces/comments (do not break the chain)
            if token in Comment or token is Text or token is Whitespace:
                yield index, token, value
                continue
            
            val_upper = value.upper()

            if token is Name or token is Name.Builtin:
                # A. If waiting for a method after a dot (DBMS_OUTPUT.PUT_LINE)
                if package_chain_state == 2:
                    # Выделяем метод пакета как Name.Function
                    yield index, Name.Function, value
                    package_chain_state = 0
                    continue

                # B. Check for package prefix (DBMS_..., UTL_...)
                # Use tuple for fast multi-option check
                if val_upper.startswith(PACKAGE_PREFIXES_TUPLE):
                    # Выделяем имя пакета как Name.Namespace
                    yield index, Name.Namespace, value
                    package_chain_state = 1 # Mark: this is a package
                    continue
                
                # C. Check for regular keywords (types, builtins, control)
                found_match = False
                for word_set, token_type in extra_content:
                    if val_upper in word_set:
                        yield index, token_type, value
                        found_match = True
                        break
                
                if found_match:
                    package_chain_state = 0
                    continue

                # D. Plain identifier (variable, column, table name)
                package_chain_state = 0
                yield index, token, value

            elif token is Punctuation and value == '.':
                if package_chain_state == 1:
                    package_chain_state = 2 # Package was seen, now we expect a method
                else:
                    package_chain_state = 0
                yield index, token, value
            
            else:
                package_chain_state = 0
                yield index, token, value
