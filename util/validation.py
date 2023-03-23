import util.utils as util

def verify_user(conn, email):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM Kunde WHERE epost=?"
    params = (email,)
    cursor.execute(query, params)
    return cursor.fetchone()[0] > 0

def verify_stasjon(conn, station):
    c = conn.cursor()
    c.execute("SELECT * FROM Jernbanestasjon WHERE navn=?", (station,))
    return c.fetchone() is not None

def verify_stasjoner(conn, togrute_id, startstasjon, endestasjon):
    if not startstasjon:
        print("Du må velge en startstasjon")
        return False
    if not endestasjon:
        print("Du må velge en endestasjon")
        return False
    if startstasjon == endestasjon:
        print("Startstasjon og endestasjon kan ikke være like")
        return False
    if not util.start_and_endstation_in_togrute(conn, togrute_id, startstasjon, endestasjon):
        print("Startstasjon og endestasjon må være i samme togrute")
        return False
    return True
