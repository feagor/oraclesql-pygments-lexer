# --- System Package Prefixes ---
# Used to mark Oracle system packages (e.g., in DBMS_OUTPUT.PUT_LINE)
# Pygments Token: Token.Name.Namespace
ORACLE_SYS_PCK_PREF = [
    'DBMS_', # Main 
    'UTL_',  # Utilities
    'CTX_',  # Oracle Text datatype support
    'APEX_', # Application Express
    'OWA_',  # Web applications support
]


# --- 1. Main Control Keywords ---
# Defines the main structure and operation of a SQL statement (DML, DDL).
# Pygments Token: Token.Keyword.Control
ORACLE_KEYWORDS_MAIN_CONTROL = [
    # DML/DDL/DCL
    'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'MERGE', 
    'CREATE', 'ALTER', 'DROP', 'TRUNCATE', 'RENAME', 'GRANT', 'REVOKE', 
    'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'LOCK', 'EXPLAIN', 'CONNECT', 'START', 
    'VIEW', 'SESSION', 'SYSTEM', 'PROCEDURE', 'FUNCTION', 'PACKAGE', 'TRIGGER', 'INDEX', 'SEQUENCE', 'TABLESPACE',
    
    # Main Clauses (Now combined)
    'FROM', 'WHERE', 'SET', 'GROUP', 'HAVING', 'ORDER', 'BY', 'WITH', 'FOR', 
    'UNION', 'INTERSECT', 'MINUS', 'UNIQUE', 'AS', 'INTO',
    
    # Joins (Main join keywords)
    'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'CROSS',
]

# --- 2. Auxiliary Keywords and Predicates ---
# Defines predicates, logical operators, and join conditions.
# Pygments Token: Token.Keyword.Constant
ORACLE_KEYWORDS_AUXILIARY = [
    # Predicates and Logical Operators
    'DISTINCT', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'IS', 'NULL', 'BETWEEN', 'EXISTS', 'ALL', 'ANY', 'SOME',
    
    # Join Conditions / Miscellaneous
    'ON', 'USING', 'NATURAL', 'TO', 'CASCADE', 'FORCE', 'SHARE', 'EXCLUSIVE', 'VALIDATE',
]

# --- 3. PL/SQL Keywords ---
# Defines the structure of the PL/SQL program block.
# Pygments Token: Token.Keyword.Declaration
ORACLE_KEYWORDS_PLSQL = [
    'BEGIN', 'END', 'DECLARE', 'EXCEPTION', 'WHEN', 'OTHERS', 'THEN', 'ELSIF', 'ELSE', 
    'IF', 'LOOP', 'WHILE', 'FOR', 'EXIT', 'CONTINUE', 'GOTO', 'PRAGMA', 'AUTONOMOUS',
    'BODY', 'IS', 'AS', 'RETURN', 'CONSTANT', 'ACCESS', 'ROW', 'MEMBER', 'SELF',
    'PIPEDED', 'RESULT', 'DETERMINISTIC',
]


# --- 4. Data Types and Type Declarations ---
# Pygments Token: Token.Keyword.Type
ORACLE_KEYWORDS_TYPE = [
    # Character
    'CHAR', 'VARCHAR2', 'VARCHAR', 'NCHAR', 'NVARCHAR2', 'CLOB', 'NCLOB', 'LONG',
    # Numeric (SQL)
    'NUMBER', 'INTEGER', 'INT', 'SMALLINT', 'DECIMAL', 'NUMERIC', 'FLOAT', 'REAL', 'DOUBLE PRECISION',
    # Numeric (PL/SQL)
    'PLS_INTEGER', 'BINARY_INTEGER', 'SIMPLE_INTEGER', 'BINARY_FLOAT', 'BINARY_DOUBLE',
    # Date / Time
    'DATE', 'TIMESTAMP', 'TIMESTAMP WITH TIME ZONE', 'TIMESTAMP WITH LOCAL TIME ZONE',
    'INTERVAL YEAR TO MONTH', 'INTERVAL DAY TO SECOND',
    # LOB
    'CLOB', 'NCLOB', 'BLOB', 'BFILE', 'LONG', 'LONG RAW',
    # RAW / Binary
    'RAW', 'LONG RAW',
    # ROWID
    'ROWID', 'UROWID',
    # Other
    'BOOLEAN', 'XMLTYPE', 'URITYPE', 'DBURITYPE', 'XDBURITYPE', 'ANYTYPE', 'ANYDATA', 'ANYDATASET', 'MLSLABEL',
]


# --- 5. Built-in Functions and Pseudo-Columns ---
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
