import mariadb
import sys
import config

# Create connection to MariaDB
# Input: -
# Returns: connection pointer
def createConnection(): 
    try:
        conn = mariadb.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    
    return conn

# Destroy connection to MariaDB
# Input: connection pointer
# Return: -
def destroyConnection(conn): 
    conn.commit()
    conn.close()

# Executes SQL-Statement with x params
# Input: connection pointer, string with SQL-statement, parameter
# Returns: cursor with SQL-Response
def executeSQL(conn, sql, *params): 
    cur = conn.cursor()
    cur.execute(sql,params)
    return cur
