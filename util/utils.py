import pandas as pd
from tabulate import tabulate

def get_path(conn, start_station, end_station, banestrekning):
    if not station_does_exist(conn, start_station):
        print(f"{start_station} er ikke en registrert stasjon")
        return None
    if not station_does_exist(conn, end_station):
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

def path_contains_path(conn, path1, path2):
    for station in path1:
        if station not in path2:
            return False
    return True
    
def station_does_exist(conn, station):
    c = conn.cursor()
    c.execute("SELECT * FROM Jernbanestasjon WHERE navn=?", (station,))
    return c.fetchone() is not None

def verify_user(conn, navn, mobilnummer):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM Kunde WHERE navn=? AND mobilnummer=?"
    params = (navn, mobilnummer)
    cursor.execute(query, params)
    return cursor.fetchone()[0] > 0

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
    if not start_and_endstation_in_togrute(conn, togrute_id, startstasjon, endestasjon):
        print("Startstasjon og endestasjon må være i samme togrute")
        return False
    return True

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
    return ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"][num]

def find_togrute(conn, startstasjon, endestasjon):
    cursor = conn.cursor()
    query = "SELECT * FROM Togrute"
    params = (startstasjon, endestasjon)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    for togrute in rows:
        if start_and_endstation_in_togrute(conn, togrute[0], startstasjon, endestasjon):
            return togrute

    return None

def get_all_seats(conn, togrute_id, date):
    cursor = conn.cursor()
    query = """
    SELECT plass_nummer, vogn_nummer
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

    # print("All seats:")
    # df = pd.DataFrame(seats, columns=["Plassnummer", "Inndeling", "Vogn"])
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def get_kunde_ordre_by_togruteforekomst(conn, togrute_id, date):
    cursor = conn.cursor()
    query = """
    SELECT pastigningstasjon_navn, avstigningstasjon_navn, plass_nummer, vogn_nummer
    FROM Kundeordre
    JOIN Togruteforekomst ON Kundeordre.togruteforekomst_dato = Togruteforekomst.dato AND Kundeordre.togrute_id = Togruteforekomst.togrute_id
    NATURAL JOIN Billett
    WHERE Kundeordre.togrute_id = ? AND Kundeordre.togruteforekomst_dato = ?
    """
    params = (togrute_id, date)
    cursor.execute(query, params)
    seats = cursor.fetchall()

    return seats
    
    # print("Taken seats:")
    # df = pd.DataFrame(seats, columns=["Påstigningstasjon", "Avstigningstasjon", "Plassnummer", "Vogn"])
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def is_overlapping_routes(conn, start1, end1, start2, end2, banestrekning):
    path1 = get_path(conn, start1, end1, banestrekning)
    path2 = get_path(conn, start2, end2, banestrekning)
    print(f"start 1: {start1}, end 1: {end1}")
    print(path1)
    print(path2)

    return any(pair in path1 for pair in path2)

def get_overlapping_kundeordre(conn, togrute_id, date, startstasjon, endestasjon):
    kundeordrer = get_kunde_ordre_by_togruteforekomst(conn, togrute_id, date)
    
    return [x for x in kundeordrer if is_overlapping_routes(conn, x[0], x[1], startstasjon, endestasjon)]

def get_available_seats(conn, togrute_id, date, startstasjon, endestasjon):
    togrute = get_togrute(conn, togrute_id)
    togrute_start = togrute[2]
    togrute_end = togrute[3]

    if startstasjon == endestasjon or not is_overlapping_routes(conn, togrute_start, togrute_end, startstasjon, endestasjon):
        return []

    all_seats = get_all_seats(conn, togrute_id, date)
    taken_seats = list(map(lambda x: (x[2], x[3]), get_overlapping_kundeordre(conn, togrute_id, date, startstasjon, endestasjon)))

    return [x for x in all_seats if x not in taken_seats]

def print_available_seats(conn, togrute_id, date, startstasjon, endestasjon):
    seats = get_available_seats(conn, togrute_id, date, startstasjon, endestasjon)

    print("Available seats:")
    df = pd.DataFrame(seats, columns=["Plassnummer", "Vogn"])
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def is_valid_path(conn, startstasjon, endestasjon, banestrekning_navn, main_direction = True):
    c = conn.cursor()
    query = """
    SELECT *
    FROM Banestrekning
    WHERE banestrekning_navn = ?
    """
    c.execute(query, (banestrekning_navn,))
    banestrekning = c.fetchone()

    if banestrekning is None:
        print(f"Banestrekning {banestrekning_navn} eksisterer ikke")
        return False

    banestrekning_start = banestrekning[1]
    banestrekning_end = banestrekning[2]

    path = get_path(conn, startstasjon, endestasjon, banestrekning)
    banestrekning_path = get_path(conn, banestrekning_start, banestrekning_end, banestrekning_navn)

    if not main_direction:
        banestrekning_path = list(map(lambda x: (x[1], x[0]), banestrekning_path))[::-1]

    if path is None or banestrekning_path is None:
        print(f"Enten {startstasjon} eller {endestasjon} eller {banestrekning_navn} er ikke gyldig")
        return False
    
    return all([segment in banestrekning_path for segment in path])

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