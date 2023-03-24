import datetime
import util.validation as val

def get_path(conn, start_station, end_station, banestrekning):
    if not val.verify_stasjon(conn, start_station):
        print(f"{start_station} er ikke en registrert stasjon")
        return None
    if not val.verify_stasjon(conn, end_station):
        print(f"{end_station} er ikke en registrert stasjon")
        return None

    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT startstasjon_navn, endestasjon_navn
    FROM Delstrekning
    JOIN Strekker_over
        ON startstasjon_navn = delstrekning_startstasjon
            AND endestasjon_navn = delstrekning_endestasjon
    WHERE banestrekning_navn=?
    """, (banestrekning,))
    rows = cursor.fetchall()
    rows = rows + [(x[1], x[0]) for x in rows]


    def traverse(start_segment, end, temp_rows):
        path = [start_segment]
        while path[-1][1] != end:
            next_list = [x for x in temp_rows if x[0] == path[-1][1] and x[1] != path[-1][0]]
            if not next_list:
                return None
            temp_rows.remove(next_list[0])
            path.append(next_list[0])

        return path

    start_list = [x for x in rows if x[0] == start_station]
    if not start_list:
        print("Det finnes ikke en delstrekning fra denne startstasjonen")
        return None
    if len(start_list) == 1:
        starting_segment = start_list[0]
        result = traverse(starting_segment, end_station, rows)
        if result:
            return result
    else:
        for starting_segment in start_list:
            rows.remove(starting_segment)
        
        for starting_segment in start_list:
            result = traverse(starting_segment, end_station, rows)
            if result:
                return result
    
    print("Det finnes ingen mulig rute mellom disse stasjonene")
    return None

def start_and_endstation_in_togrute(conn, togrute_id, startstasjon, endestasjon, banestrekning):
    togrute_obj = get_togrute(conn, togrute_id)
    togrute_start = togrute_obj[2]
    togrute_end = togrute_obj[3]
    togrute_path = get_path(conn, togrute_start, togrute_end, banestrekning)

    startstasjon_in_togrute = filter(lambda x: x[0] == startstasjon, togrute_path) is not None
    endestasjon_in_togrute = filter(lambda x: x[1] == endestasjon, togrute_path) is not None

    return startstasjon_in_togrute and endestasjon_in_togrute

def get_togrute(conn, togrute_id):
    cursor = conn.cursor()
    query = "SELECT * FROM Togrute WHERE togrute_id=?"
    cursor.execute(query, (togrute_id,))
    return cursor.fetchone()

def number_to_day(num):
    if num < 0 or num > 6:
        return None
    return ["søndag", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag"][num]

def get_all_seats(conn, togrute_id, date):
    cursor = conn.cursor()
    query = """
    SELECT vogn_nummer, plass_nummer, inndeling_nummer, vogn_type
    FROM Togrute
    NATURAL JOIN Togruteforekomst
    NATURAL JOIN Vognoppsett
    NATURAL JOIN Vogn
    NATURAL JOIN Plass
    WHERE dato = ? AND togrute_id = ?
    """
    params = (date, togrute_id)
    cursor.execute(query, params)
    seats = cursor.fetchall()
    
    return seats

def get_kunde_ordre_by_togruteforekomst(conn, togrute_id, date):
    cursor = conn.cursor()
    query = """
    SELECT pastigningstasjon_navn, avstigningstasjon_navn, plass_nummer, vogn_nummer, vogn_type, banestrekning_navn, inndeling_nummer
    FROM Kundeordre
    JOIN Togruteforekomst ON Kundeordre.togruteforekomst_dato = Togruteforekomst.dato AND Kundeordre.togrute_id = Togruteforekomst.togrute_id
    NATURAL JOIN Billett
    NATURAL JOIN Vogn
    NATURAL JOIN Togrute
    NATURAL JOIN Plass
    WHERE Kundeordre.togrute_id = ? AND Kundeordre.togruteforekomst_dato = ?
    """
    params = (togrute_id, date)
    cursor.execute(query, params)
    seats = cursor.fetchall()

    return seats
    
def is_overlapping_routes(conn, start1, end1, start2, end2, banestrekning):
    path1 = get_path(conn, start1, end1, banestrekning)
    path2 = get_path(conn, start2, end2, banestrekning)

    return any(pair in path1 for pair in path2)

def get_overlapping_kundeordre(conn, togrute_id, date, startstasjon, endestasjon):
    kundeordrer = get_kunde_ordre_by_togruteforekomst(conn, togrute_id, date)
    new_kundeordrer = []
    for kundeordre in kundeordrer:
        if kundeordre[4] == "sitte": continue

        if is_adjacent_bed_taken(kundeordre[2], kundeordre[3], kundeordre[6], kundeordrer):
            continue

        offset = 1 if kundeordre[2] % 2 == 1 else -1
        new_kundeordre = (kundeordre[0], kundeordre[1], kundeordre[2] + offset, kundeordre[3], kundeordre[4], kundeordre[5], kundeordre[6])
        if new_kundeordre not in kundeordrer:
            new_kundeordrer.append(new_kundeordre)

    kundeordrer += new_kundeordrer
    return [x for x in kundeordrer if is_overlapping_routes(conn, x[0], x[1], startstasjon, endestasjon, x[5]) or x[4] == "sove"]

def get_available_seats(conn, togrute_id, date, startstasjon, endestasjon):
    togrute = get_togrute(conn, togrute_id)
    togrute_start = togrute[2]
    togrute_end = togrute[3]

    if startstasjon == endestasjon or not is_overlapping_routes(conn, togrute_start, togrute_end, startstasjon, endestasjon, togrute[4]):
        return []

    all_seats = get_all_seats(conn, togrute_id, date)
    taken_seats = list(map(lambda x: (x[3], x[2], x[6], x[4]), get_overlapping_kundeordre(conn, togrute_id, date, startstasjon, endestasjon)))

    return [x for x in all_seats if x not in taken_seats]

def is_within_togrute(conn, togrute_id, startstasjon, endestasjon):
    togrute = get_togrute(conn, togrute_id)
    togrute_start = togrute[2]
    togrute_end = togrute[3]

    togrute_path = get_path(conn, togrute_start, togrute_end, togrute[4])
    path = get_path(conn, startstasjon, endestasjon, togrute[4])

    return all([segment in togrute_path for segment in path])

def get_containing_togruter(conn, startstasjon, endestasjon):
    c = conn.cursor()
    query = """
    SELECT togrute_id, dato, startstasjon, endestasjon, togrute_navn, banestrekning_navn
    FROM Togrute
    NATURAL JOIN Togruteforekomst
    """
    c.execute(query)
    togruter = c.fetchall()

    return [x for x in togruter if is_within_togrute(conn, x[0], startstasjon, endestasjon)]

def compareDates(date_time, input_date, input_time):
        date_time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        
        input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d")
        input_time = datetime.datetime.strptime(input_time, "%H:%M")
        input_date_time = datetime.datetime.combine(input_date, input_time.time())

        if date_time > input_date_time:
            return 1
        elif date_time == input_date_time:
            return 0
        else:
            return -1


def get_weekday_number(weekday_string):
    weekdays = ["søndag", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag"]
    return weekdays.index(weekday_string)

def get_next_ordre_nummer(conn):
    c = conn.cursor()
    query = """
    SELECT MAX(ordre_nummer)
    FROM KundeOrdre
    """
    c.execute(query)
    max_ordre_nummer = c.fetchone()[0]
    if max_ordre_nummer is None:
        return 1
    else:
        return max_ordre_nummer + 1

def get_kunde_nummer(conn, email):
    c = conn.cursor()
    query = """
    SELECT kunde_nummer
    FROM Kunde
    WHERE epost = ?
    """
    c.execute(query, (email,))
    kunde_nummer = c.fetchone()
    if kunde_nummer is None:
        return None
    else:
        return kunde_nummer[0]

def is_adjacent_bed_taken(plass_nummer, vogn_nummer, inndeling_nummer, objs):
    return any([x[3] == vogn_nummer and x[6] == inndeling_nummer and x[2] != plass_nummer for x in objs])

def get_correct_date(startstasjon_dato, startstasjon_rutetid, avgangstasjon_rutetid):
    if(startstasjon_rutetid > avgangstasjon_rutetid):
        startstasjon_dato = datetime.datetime.strptime(startstasjon_dato, "%Y-%m-%d")
        startstasjon_dato += datetime.timedelta(days=1)
        startstasjon_dato = startstasjon_dato.strftime("%Y-%m-%d")
    return startstasjon_dato