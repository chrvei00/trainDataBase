import sqlite3
import datetime
import math


def search_togruter(conn, start_stasjon, ende_stasjon, dato, klokkeslett):
    c = conn.cursor()
    c.execute("SELECT togrute_id, delstrekning_startstasjon, delstrekning_endestasjon FROM Togrute NATRUAL JOIN Strekker_over")
    togruter = c.fetchall()
    potential_togruter = []
    for togrute in togruter:
        pass
    

def register_kunde(conn, navn, epost, mobilnummer):
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO kunde (navn, epost, mobilnummer) VALUES (?, ?, ?)",
            (navn, epost, mobilnummer)
        )
        conn.commit()
        print("\nKunde registrert.")
    except sqlite3.IntegrityError:
        print("\nKunden finnes allerede i databasen.")
        return False


def create_vogn_and_plasser(conn, type, vogn_nr, vognoppsett_id, sections, seats_per_section):
    try:
        c = conn.cursor()
        c.execute(
            '''
            INSERT INTO
                Vogn (
                    vogn_nummer,
                    vognoppsett_id,
                    vogn_type,
                    antall_plasser,
                    antall_inndelinger
                )
            VALUES
                (?, ?, ?, ?, ?);
            ''',
            (vogn_nr, vognoppsett_id, type, seats_per_section, sections)
        )

        for seat_idx in range(1, sections * seats_per_section + 1):
            c.execute(
                "INSERT INTO Plass VALUES (?, ?, ?, ?);",
                (vognoppsett_id, vogn_nr, seat_idx, math.ceil(seat_idx / seats_per_section))
            )
        conn.commit()
            
    except sqlite3.Error as e:
        print("Klarer ikke opprette plasser.")
        print(e)
    
def get_togruter(conn, stasjon, ukedag):
    # TODO
    print("Få togruter")

def registrer_kunde(conn, navn, email, mobilnummer):
    # TODO
    print("Registrer kunde")