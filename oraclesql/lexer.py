from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name

from oraclesql._oraclesql_builtins import ORACLE_KEYWORDS, ORACLE_PLSQL_KEYWORDS

ORACLE_KEYWORDS += ORACLE_PLSQL_KEYWORDS

__all__ = ["OracleSQLLexer"]


# TODO: Use a custom lexer for SQL
class OracleSQLLexer(SqlLexer):
    name = "Oracle PL/SQL"
    aliases = ["oraclesql"]
    mimetypes = ["text/x-oracle-plsql"]

    def get_tokens_unprocessed(self, text):
        extra_content = [(ORACLE_KEYWORDS, Keyword)]

        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                for i in extra_content:
                    if value in i[0]:
                        yield index, i[1], value
                        break
                else:
                    yield index, token, value
            else:
                yield index, token, value
