from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name

from oraclesql._oraclesql_builtins import ORACLE_KEYWORDS, ORACLE_PLSQL_KEYWORDS, ORACLE_DATATYPES

# Объединяем ключевые слова в один Set для скорости (O(1) поиск)
ALL_KEYWORDS = set(ORACLE_KEYWORDS + ORACLE_PLSQL_KEYWORDS)
# Типы данных тоже в Set
ALL_TYPES = set(ORACLE_DATATYPES)

__all__ = ["OracleSQLLexer"]

class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        # Определяем приоритет проверки:
        # Сначала проверяем Типы, потом Ключевые слова
        extra_content = [
            (ALL_TYPES, Name.Builtin),
            (ALL_KEYWORDS, Keyword)
        ]

        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            # Проверяем токены, которые SqlLexer посчитал "Именем" (Name)
            if token is Name or token is Name.Builtin:
                # ВАЖНО: Приводим к верхнему регистру для проверки!
                val_upper = value.upper()
                
                found_match = False
                for word_set, token_type in extra_content:
                    if val_upper in word_set:
                        yield index, token_type, value
                        found_match = True
                        break
                
                if not found_match:
                    yield index, token, value
            else:
                yield index, token, value

