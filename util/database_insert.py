import sqlite3

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
    except sqlite3.Error:
        print("Klarer ikke opprette plasser.")
        conn.rollback()