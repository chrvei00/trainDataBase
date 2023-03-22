import sqlite3
import datetime
import pandas as pd
import util.utils as utils
from tabulate import tabulate

def print_togruter_by_stasjoner_and_date(conn, start_stasjon, ende_stasjon, dato):
    try:
        print("\nSøker etter togruter fra " + start_stasjon + " til " + ende_stasjon + " på datoen " + dato + "...\n")
        
        #Finn datoene
        date_obj = datetime.datetime.strptime(dato, "%Y-%m-%d")
        next_date_obj = date_obj + datetime.timedelta(days = 1)
        next_date = next_date_obj.strftime("%Y-%m-%d")
        
        togruter = utils.get_containing_togruter(conn, start_stasjon, ende_stasjon)
        togruter = list(filter(lambda x: x[1] == dato or x[1] == next_date, togruter))

        togruter = list(map(
            lambda x: [*x, get_rutetid_by_togrute_and_stasjon(conn, x[0], start_stasjon)], togruter))


        #Sorterer togruter etter avgangstid fra startstasjon
        togruter.sort(key=lambda x: x[6])
        togruter.sort(key=lambda x: x[1])

        if togruter == []:
            print("Fant ingen togruter fra " + start_stasjon + " til " + ende_stasjon + " på datoen " + dato + ".")

        #Finner alle togruter som har en delstrekning som går mellom start og endestasjon
        df = pd.DataFrame(togruter)
        
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        return True
    except sqlite3.Error as e:
        print("\nKlarte ikke finne noen togruter mellom stasjonene")
        return False

def get_rutetid_by_togrute_and_stasjon(conn, togrute_id, stasjon):
    try:
        c = conn.cursor()
        c.execute("SELECT avgang_tid FROM Rute_tid WHERE togrute_id = ? AND jernbanestasjon_navn = ?", (str(togrute_id), stasjon))
        return c.fetchone()
    except sqlite3.Error:
        return None      

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
    return True

def get_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag):
    if ukedag != None:
        print("\nHenter togruter for stasjon", stasjon, "på", utils.number_to_day(int(ukedag)), "...\n")
    try:
        c = conn.cursor()
        c.execute("""
            SELECT togrute_id, dato, startstasjon, endestasjon, togrute_navn, banestrekning_navn
            FROM Togrute
            NATURAL JOIN Togruteforekomst
        """)
        togruter = c.fetchall()

        paths = [(utils.get_path(conn, x[2], x[3], x[5]), i) for i, x in enumerate(togruter)]
        paths = list(filter(lambda x: any([y[0] == stasjon or y[1] == stasjon for y in x[0]]), paths))

        togruter = [togruter[x[1]] for x in paths]

        if ukedag != None:
            togruter = filter(lambda rute: datetime.datetime.strptime(rute[1], "%Y-%m-%d").weekday() == int(ukedag), togruter)
        return list(togruter)
    except sqlite3.IntegrityError as e:
       return False

def print_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag):
    try:
        togruter = get_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag)
        df = pd.DataFrame(togruter, columns=["id", "Dato", "Startstasjon", "Endestasjon", "Togrutenavn", "Banestrekningnavn"])
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    except sqlite3.IntegrityError as e:
        print("Noe gikk galt ved henting av togruter:", e)

def print_orders(conn, navn, mobilnummer):
    try:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM Kunde NATURAL JOIN Kundeordre WHERE navn = ? AND mobilnummer = ?",
            (navn, mobilnummer)
        )
        orders =  c.fetchall()
        df = pd.DataFrame(orders, columns=["Ordrenummer", "Kjopsdato", "Kundenummer", "Togrute_dato", "Togrute_id", "Til", "Fra"])
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        return True
    except sqlite3.Error:
        print("Klarer ikke å hente bestillinger.")
        return False