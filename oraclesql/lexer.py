from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name, Punctuation, Text, Whitespace, Comment

# 1. Импортируем новый список
from oraclesql._oraclesql_builtins import (
    ORACLE_KEYWORDS, 
    ORACLE_PLSQL_KEYWORDS, 
    ORACLE_DATATYPES, 
    ORACLE_PACKAGE_PREFIXES  # <-- Новый импорт
)

ALL_KEYWORDS = set(ORACLE_KEYWORDS + ORACLE_PLSQL_KEYWORDS)
ALL_TYPES = set(ORACLE_DATATYPES)

# 2. Превращаем список префиксов в кортеж (tuple), 
# так как startswith() принимает именно tuple.
PACKAGE_PREFIXES_TUPLE = tuple(ORACLE_PACKAGE_PREFIXES)

__all__ = ["OracleSQLLexer"]

class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        extra_content = [
            (ALL_TYPES, Name.Builtin),
            (ALL_KEYWORDS, Keyword)
        ]

        # 0=ничего, 1=пакет, 2=точка (ждем метод)
        package_chain_state = 0

        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            # Пропуск пробелов/комментариев (не ломаем цепочку)
            if token in Comment or token is Text or token is Whitespace:
                yield index, token, value
                continue
            
            val_upper = value.upper()

            if token is Name or token is Name.Builtin:
                # А. Если ждем метод после точки (DBMS_OUTPUT . <PUT_LINE>)
                if package_chain_state == 2:
                    yield index, Name.Namespace, value
                    package_chain_state = 0
                    continue

                # Б. Проверяем префикс пакета (DBMS_..., UTL_...)
                # Используем кортеж для быстрой проверки всех вариантов разом
                if val_upper.startswith(PACKAGE_PREFIXES_TUPLE):
                    yield index, Name.Namespace, value
                    package_chain_state = 1 # Запоминаем: это пакет
                    continue
                
                # В. Обычные проверки (типы, кейворды)
                found_match = False
                for word_set, token_type in extra_content:
                    if val_upper in word_set:
                        yield index, token_type, value
                        found_match = True
                        break
                
                if found_match:
                    package_chain_state = 0
                    continue

                # Г. Просто имя
                package_chain_state = 0
                yield index, token, value

            elif token is Punctuation and value == '.':
                if package_chain_state == 1:
                    package_chain_state = 2 # Пакет был, теперь точка
                else:
                    package_chain_state = 0
                yield index, token, value
            
            else:
                package_chain_state = 0
                yield index, token, value
