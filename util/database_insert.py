import sqlite3
import math

def insert_Kunde(conn, kunde_nummer, navn, epost, mobilnummer):
    try:
        c = conn.cursor()
        c.execute(
            '''
            INSERT INTO
                Kunde (
                    kunde_nummer,
                    navn,
                    epost,
                    mobilnummer
                )
            VALUES
                (?, ?, ?, ?);
            ''',
            (kunde_nummer, navn, epost, mobilnummer)
        )
        conn.commit()      
    except sqlite3.Error:
        print("Klarer ikke opprette kunde.")
        conn.rollback()

def insert_Kundeordre(conn, ordre_nummer, kjop_datotid, kunde_nummer, togruteforekomst_dato, togrute_id, pastigningsstasjon_navn, avstigningstasjon_navn):
    try:
        c = conn.cursor()
        c.execute(
            '''
            INSERT INTO
                Kundeordre (
                    ordre_nummer,
                    kjop_datotid,
                    kunde_nummer,
                    togruteforekomst_dato,
                    togrute_id,
                    pastigningstasjon_navn,
                    avstigningstasjon_navn
                )
            VALUES
                (?, ?, ?, ?, ?, ?, ?);
            ''',
            (ordre_nummer, kjop_datotid, kunde_nummer, togruteforekomst_dato, togrute_id, pastigningsstasjon_navn, avstigningstasjon_navn)
        )
        conn.commit()      
    except sqlite3.Error:
        print("Klarer ikke opprette plasser.")
        conn.rollback()

def insert_Billett(conn, vognoppsett_id, vogn_nummer, plass_nummer, ordre_nummer):
    try:
        c = conn.cursor()
        c.execute(
            '''
            INSERT INTO
                Billett (
                    vognoppsett_id,
                    vogn_nummer,
                    plass_nummer,
                    ordre_nummer
                )
            VALUES
                (?, ?, ?, ?);
            ''',
            (vognoppsett_id, vogn_nummer, plass_nummer, ordre_nummer)
        )
        conn.commit()  
        return True    
    except sqlite3.Error:
        print("Klarer ikke opprette plasser.")
        conn.rollback()

def insert_vogn_and_plasser(conn, type, vogn_nr, vognoppsett_id, sections, seats_per_section):
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
            
    except sqlite3.Error:
        print("Klarer ikke opprette plasser.")
        conn.rollback()


def insert_delstrekning(conn, startstasjon, endestasjon, avstand):
    try:
        c = conn.cursor()
        cursor = c.execute("INSERT INTO Delstrekning VALUES (?, ?, ?)", (endestasjon, startstasjon, avstand))
        c.commit()
    except Exception as e:
        print(e)
        return False