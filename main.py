import os
import util.database_connect as dbc
import util.cli_program as cli
import util.utils as utils

def main():
    database = "./database/jernbanedatabase.db"
 
    #Connect to database
    conn = None
    if not os.path.exists(database):
        print("Initializing database")
        conn = dbc.create_connection(database)
        dbc.init_database(conn, './scripts/init_traindatabase.sql')
        dbc.insert_defaultvalues(conn, './scripts/insertdata_nordlandsbanen_traindatabase.sql')
    else:
        print("Connecting to database")
        conn = dbc.create_connection(database)

    print(utils.getPath(conn, "Steinkjer", "Mo i Rana"))

    # Run program
    cli.start(conn)

    #Close connection
    conn.close()

main()