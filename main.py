import os
import util.database_connect as dbc
import util.cli_program as cli

def main():
    database = "./database/traindatabase.db"
 
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


    # Run program
    cli.start(conn)

    #Close connection
    conn.close()

main()