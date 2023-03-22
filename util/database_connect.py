import sqlite3
import util.database_functions as dbf
import util.database_insert as dbi

def init_database(conn, script_path):
    try:
        with open(script_path, 'r') as f:
            sql_script = f.read()
        c = conn.cursor()
        c.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        conn.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        print(e)
    return conn

def insert_defaultvalues(conn, script_path):
    try:
        with open(script_path, 'r') as f:
            sql_script = f.read()
        c = conn.cursor()
        c.executescript(sql_script)
        conn.commit()

        vogner = [
            ("sitte", 1, 1, 3, 4),
            ("sitte", 2, 1, 3, 4),
            ("sitte", 1, 2, 3, 4),
            ("sove", 2, 2, 4, 2),
            ("sitte", 1, 3, 3, 4)
        ]
        for vogn in vogner:
            dbi.insert_vogn_and_plasser(conn, *vogn)
    
    except sqlite3.Error as e:
        print(e)
