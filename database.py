import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)    #opens the db file and returns a connection object

def setupdb():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news(
        id       INTEGER AUTOINCREMENT PRIMARY KEY
        title    STRINGS      
        )
      """  
    )
    
    conn.commit()
    conn.close()
    

