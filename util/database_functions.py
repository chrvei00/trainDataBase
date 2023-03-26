import sqlite3
import datetime
import pandas as pd
from tabulate import tabulate
from termcolor import colored
import util.utils as utils
import util.database_insert as dbi
import util.validation as val

def print_togruter_by_stasjoner_and_date(conn, start_stasjon, ende_stasjon, dato, tid):
    try:
        print(colored(f"\nSøker etter togruter fra {start_stasjon} til {ende_stasjon} på datoen {dato} etter klokken {tid}....\n", "blue"))
        
        #Finn datoene
        date_obj = datetime.datetime.strptime(dato, "%Y-%m-%d")
        next_date_obj = date_obj + datetime.timedelta(days = 1)
        next_date = next_date_obj.strftime("%Y-%m-%d")
        
        togruter = utils.get_containing_togruter(conn, start_stasjon, ende_stasjon)

        togruter = list(map(
            lambda x: [*x, get_rutetid_by_togrute_and_stasjon(conn, x[0], start_stasjon)[0]], togruter))
            

        if togruter == []:
            print(colored(f"Fant ingen togruter fra {start_stasjon} til {ende_stasjon} på datoen {dato} etter klokken {tid}.", "red"))
            return

        togruter = map(lambda x: (x[0], f"{x[4]} - {x[2]} ➢ {x[3]}", x[5], start_stasjon, ende_stasjon, utils.get_correct_date(x[1], get_rutetid_by_togrute_and_stasjon(conn, x[0], x[2])[0], x[6]) + " " + x[6], x[1]), togruter)

        #Sort and filter
        togruter = list(filter(lambda x: utils.compareDates(x[5], dato, tid) >= 0, togruter))
        togruter = list(filter(lambda x: x[5][0:10] == dato or x[5][0:10] == next_date, togruter))
        togruter.sort(key=lambda x: (x[5]))

        # Assigns the index to the id field for printing purposes
        new_togruter = [(str(i), x[1], x[2], x[3], x[4], x[5]) for i, x in enumerate(togruter)]

        #Finner alle togruter som har en delstrekning som går mellom start og endestasjon
        df = pd.DataFrame(new_togruter, columns=["id", "Togrute", "Banestrekning", "Påstigningstasjon", "Avstigningstasjon", f"Avgang {start_stasjon}"])
        
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        return togruter
    except sqlite3.Error as e:
        print(colored("\nKlarte ikke finne noen togruter mellom stasjonene", "red"))
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
    except sqlite3.IntegrityError:
        print(colored("\nKunden finnes allerede i databasen.", "red"))
        return False
    return True

def get_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag):
    if ukedag != None:
        print(colored(f"\nHenter togruter for stasjon {stasjon} på {utils.number_to_day(int(ukedag))}...\n", "blue"))
    try:
        c = conn.cursor()
        togruter = utils.get_all_togruter(conn)

        paths = [(utils.get_path(conn, x[1], x[2], x[3]), i) for i, x in enumerate(togruter)]
        paths = list(filter(lambda x: any([y[0] == stasjon or y[1] == stasjon for y in x[0]]), paths))
        togruter_ids = [togruter[x[1]][0] for x in paths]

        togruter = []
        for x in togruter_ids:
            c.execute(
            """
            SELECT togrute_id, startstasjon, endestasjon, togrute_navn, banestrekning_navn
            FROM Togrute
            NATURAL JOIN (
                SELECT date(dato, '+' || dager_etter_avgangsdato || ' days') as new_date, togrute_id
                FROM Togruteforekomst
                NATURAL JOIN Rute_tid
                WHERE jernbanestasjon_navn = ?
                )
            WHERE togrute_id = ?
                AND strftime('%w', new_date) = ?
            """, (stasjon, x, ukedag))
            
            rute = c.fetchone()
            if rute:
                togruter.append(rute)

        return list(togruter)
    except sqlite3.IntegrityError as e:
       return False

def print_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag):
    if val.verify_weekday_string(ukedag):
        ukedag = str(utils.get_weekday_number(ukedag))
    try:
        togruter = get_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag)
        togruter = list(map(lambda x: (x[0], x[1], x[2], x[3], x[4]), togruter))
        if togruter == []:
            print(colored(f"Fant ingen togruter for stasjon {stasjon} på {utils.number_to_day(int(ukedag))}.", "red"))
            return
        df = pd.DataFrame(togruter, columns=["id", "Startstasjon", "Endestasjon", "Togrute", "Banestrekningnavn"])
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    except sqlite3.IntegrityError as e:
        print(colored("Noe gikk galt ved henting av togruter:", "red"))

def print_orders(conn, epost):
    try:
        c = conn.cursor()
        c.execute(
            """
            SELECT ordre_nummer, kjop_datotid, togrute_id, togruteforekomst_dato, pastigningstasjon_navn, avstigningstasjon_navn, vogn_nummer, plass_nummer 
            FROM Kunde NATURAL JOIN Kundeordre 
            NATURAL JOIN Billett
            WHERE epost = ? AND kjop_datotid > CURRENT_TIMESTAMP
            """,
            (epost,)
        )
        orders =  c.fetchall()
        df = pd.DataFrame(orders, columns=["Ordrenummer", "Kjopsdato", "Togrute_id", "Togrute_dato", "Til", "Fra", "Vognnummer", "Plassnummer"])
        if (orders == []):
            print(colored("Fant ingen bestillinger.", "red"))
            return False
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        return True
    except sqlite3.Error:
        print(colored("Klarer ikke å hente bestillinger.", "red"))
        return False

def print_available_seats(conn, togrute_id, date, startstasjon, endestasjon):
    seats = utils.get_available_seats(conn, togrute_id, date, startstasjon, endestasjon)

    print(colored("Available seats:", "green"))
    df = pd.DataFrame(seats, columns=["Vogn", "Plassnummer", "Inndeling", "Setetype"])
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    return seats

def buy_billett(conn, togrute_id, vogn, plass, ordre_nummer):
    if not dbi.insert_Billett(conn, togrute_id, vogn, plass, ordre_nummer):
        print(colored("Klarte ikke å kjøpe billett.", "red"))
        return False
    print(colored("Billett kjøpt.", "green"))
    return True

def create_ordre(conn, togrute_id, dato, email, pastigningsstasjon_navn, avstigningstasjon_navn):
    kunde_nummer = utils.get_kunde_nummer(conn, email)
    ordre_nummer = utils.get_next_ordre_nummer(conn)
    kjop_datotid = datetime.datetime.now()
    dbi.insert_Kundeordre(conn, ordre_nummer, kjop_datotid, kunde_nummer, dato, togrute_id, pastigningsstasjon_navn, avstigningstasjon_navn)
    return ordre_nummer
