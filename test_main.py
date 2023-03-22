import os
import util.database_connect as dbc
import util.utils as utils
import util.database_insert as dbi


def main():
    database = "./database/test_jernbanedatabase.db"

    # Connect to database
    conn = None
    if not os.path.exists(database):
        print("Initializing database")
        conn = dbc.create_connection(database)
        dbc.init_database(conn, './scripts/init_traindatabase.sql')
        dbc.insert_defaultvalues(
            conn, './scripts/insertdata_nordlandsbanen_traindatabase.sql')
    else:
        print("Connecting to database")
        conn = dbc.create_connection(database)

    # Insert test data
    # dbi.insert_Kunde(conn, 1, "Ola Nordmann", "ola.nordmann@fuckyou.com", "12345678")
    dbi.insert_Kundeordre(conn, 2, "2023-03-23 15:00:00", 1, "2023-04-03", 1, "Mosjøen", "Bodø")
    dbi.insert_Billett(conn, 1, 1, 1, 2)
    
    
    # Test functions
    # utils.print_available_seats(conn, 1, "2023-04-03", "Trondheim S", "Bodø")
    print(utils.get_path(conn, "Bodø", "Trondheim S", "Nordlandsbanen"))
    

    # Close connection
    conn.close()


main()

