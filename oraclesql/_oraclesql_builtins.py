# --- System Package Prefixes (Required by User) ---
# Used in lexer rules to highlight common system calls.
# Pygments Token: Token.Name.Builtin.System (or similar)
ORACLE_SYS_PCK_PREF = [
    'DBMS_', # Main 
    'UTL_',  # Utils
    'CTX_',  # Oracle Text datatype support
    'APEX_', # Application Express
    'OWA_',  # Web applications support
]


# --- 1. Control Keywords (SQL DDL, DML, DCL, and Clauses) ---
# Defines the structure of the query or operation.
# Pygments Token: Token.Keyword.Control
ORACLE_KEYWORDS_CONTROL = [
    # DDL/DML/DCL (Main Operators)
    'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'MERGE', 'FROM', 'WHERE', 'SET', 
    'CREATE', 'ALTER', 'DROP', 'TRUNCATE', 'RENAME', 'GRANT', 'REVOKE', 
    'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'LOCK', 'EXPLAIN', 'CONNECT', 'START', 
    'VIEW', 'SESSION', 'SYSTEM', 'PROCEDURE', 'FUNCTION', 'PACKAGE', 'TRIGGER', 'INDEX', 'SEQUENCE', 'TABLESPACE',
    
    # Predicates and Logical Operators
    'AND', 'OR', 'NOT', 'IN', 'LIKE', 'IS', 'NULL', 'BETWEEN', 'EXISTS', 'ALL', 'ANY', 'SOME',
    
    # Structural/Ordering/Grouping
    'GROUP', 'HAVING', 'ORDER', 'BY', 'WITH', 'FOR', 'UNION', 'INTERSECT', 'MINUS', 'DISTINCT', 'UNIQUE',
    
    # Joins
    'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON', 'USING', 'NATURAL', 'CROSS',
    
    # Miscellaneous
    'AS', 'TO', 'INTO', 'CASCADE', 'FORCE', 'SHARE', 'EXCLUSIVE', 'VALIDATE',
]


# --- 2. PL/SQL Keywords ---
# Defines the structure of the PL/SQL program block.
# Pygments Token: Token.Keyword.Control / Token.Keyword.Declaration
ORACLE_KEYWORDS_PLSQL = [
    'BEGIN', 'END', 'DECLARE', 'EXCEPTION', 'WHEN', 'OTHERS', 'THEN', 'ELSIF', 'ELSE', 
    'IF', 'LOOP', 'WHILE', 'FOR', 'EXIT', 'CONTINUE', 'GOTO', 'PRAGMA', 'AUTONOMOUS',
    'BODY', 'IS', 'AS', 'RETURN', 'CONSTANT', 'ACCESS', 'ROW', 'MEMBER', 'SELF',
    'PIPEDED', 'RESULT', 'DETERMINISTIC',
]


# --- 3. Data Types and Declarations (Type Keywords) ---
# Pygments Token: Token.Keyword.Type
ORACLE_KEYWORDS_TYPE = [
    # Core Data Types
    'VARCHAR2', 'NVARCHAR2', 'CHAR', 'NCHAR', 'NUMBER', 'LONG', 'DATE', 'TIMESTAMP', 
    'INTERVAL', 'CLOB', 'NCLOB', 'BLOB', 'RAW', 'ROWID', 'BOOLEAN', 
    # Specialized/PL/SQL Types
    'PLS_INTEGER', 'BINARY_INTEGER', 'BINARY_FLOAT', 'BINARY_DOUBLE', 
    # Declarations
    'TYPE', 'SUBTYPE', 'REF', 'TABLE', 'VARRAY', 'OF', 'OUT', 'IN', 'DEFAULT', 'NOCOPY',
    'XMLTYPE',
]


# --- 4. Built-in Functions and Pseudo-Columns ---
# The most common built-in functions and system variables.
# Pygments Token: Token.Name.Builtin
ORACLE_BUILTINS_NAME = [
    # Aggregate and Analytic
    'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'STDDEV', 'VARIANCE', 'LISTAGG', 
    'RANK', 'DENSE_RANK', 'ROW_NUMBER', 'CUME_DIST', 'LAG', 'LEAD', 'OVER', 'PARTITION', 'KEEP',
    
    # Conversion and Conditional
    'TO_CHAR', 'TO_DATE', 'TO_NUMBER', 'NVL', 'NVL2', 'DECODE', 'COALESCE', 'NULLIF', 'CAST', 
    'CONVERT', 'CASE', 
    
    # String Functions
    'SUBSTR', 'INSTR', 'LENGTH', 'TRIM', 'LTRIM', 'RTRIM', 'UPPER', 'LOWER', 'INITCAP', 'LPAD', 'RPAD', 
    'CONCAT', 'TRANSLATE', 'REPLACE', 'REGEXP_LIKE', 'REGEXP_SUBSTR', 'REGEXP_REPLACE', 
    
    # Date/Time
    'SYSDATE', 'SYSTIMESTAMP', 'CURRENT_DATE', 'CURRENT_TIMESTAMP', 'SESSIONTIMEZONE', 
    'DBTIMEZONE', 'ROUND', 'TRUNC', 'ADD_MONTHS', 'MONTHS_BETWEEN', 'NEXT_DAY', 'LAST_DAY',
    
    # Pseudo-Columns/Environment
    'ROWNUM', 'LEVEL', 'USER', 'UID', 'SYS_GUID', 'SQLCODE', 'SQLERRM', 
    'NEXTVAL', 'CURRVAL', 'DB_NAME', 'SESSION_USER',
]
