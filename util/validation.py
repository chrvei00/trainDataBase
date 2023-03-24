import datetime
import util.utils as utils


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

def verify_date_string(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def verify_time_string(time):
    try:
        datetime.datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False

def verify_weekday_string(weekday_string):
    return weekday_string in ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]

def verify_weekday_number(weekday_number):
    try:
        weekday_number = int(weekday_number)
    except ValueError:
        return False
    return weekday_number >= 0 and weekday_number <= 6

def verify_togrute_id(conn, togrute_id):
    return utils.get_togrute(conn, togrute_id) is not None

def verify_togruteforekomst_exists(conn, dato, togrute_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Togruteforekomst WHERE dato=? AND togrute_id=?", (dato, togrute_id))
    return c.fetchone() is not None
