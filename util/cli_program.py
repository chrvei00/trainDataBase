import util.database_functions as dbf
import util.validation as val
from termcolor import colored


def start(conn):
    while True:
        print(colored("\n=========================================\n", "magenta"))
        print(colored("Velkommen til togbillettsystemet!", "blue"))
        print(colored("\nDu kan når som helst skrive exit for å gå tilbake til hovedmenyen\n", "yellow"))
        print(colored("Velg en handling:", "blue"))
        print("1. Hent togruter for en stasjon på en ukedag")
        print("2. Søk etter togruter")
        print("3. Registrer kunde")
        print("4. Bestill billeter")
        print("5. Vis dine fremtidige reiser")
        print("0. Avslutt")

        valg = input("\nVelg handling (0-5): ")
        while not valg.isdigit() or not int(valg) in range(6):
            print(colored("Ugyldig valg. Prøv igjen.", "red"))
            valg = input("Velg handling (0-5): ")
        valg = int(valg)
        print(colored("\n-----------------------------------------\n", "magenta"))

        # Finn togruter for en stasjon på en ukedag
        if valg == 1:
            #Brukerhistorie c
            print(colored("Hent togruter for en stasjon på en ukedag", "blue"))
            hent_togruter_for_en_stasjon_på_en_ukedag(conn)
        # Søk etter togruter
        elif valg == 2:
            #Brukerhistorie d
            print(colored("Søk etter togruter", "blue"))
            søk_etter_togruter(conn)
        # Registrer kunde
        elif valg == 3:
            #Brukerhistorie e
            print(colored("Registrer kunde", "blue"))
            register_kunde(conn)
        # Bestill billeter
        elif valg == 4:
            #Brukerhistorie g
            print(colored("Bestill billeter", "blue"))
            bestill_billetter(conn)
        # Vis dine fremtidige reiser
        elif valg == 5:
            #Brukerhistorie h
            print(colored("Vis dine fremtidige reiser", "blue"))
            vis_dine_fremtidige_reiser(conn)
        elif valg == 0:
            break
        else:
            print(colored("Ugyldig valg. Prøv igjen.", "red"))

        print(colored("\n-----------------------------------------\n", "magenta"))
        if (input("\nVil du utføre en ny handling? (y/n) ") == "n"):
            break

def hent_togruter_for_en_stasjon_på_en_ukedag(conn):
    stasjon = input("Skriv inn stasjon: ")
    while not val.verify_stasjon(conn, stasjon) and not stasjon == "exit":
        print(colored("Ugyldig stasjon. Prøv igjen.", "red"))
        stasjon = input("Skriv inn stasjon: ")
    if stasjon == "exit":
        return

    ukedag = input("Skriv inn ukedag: ").lower()
    while not val.verify_weekday_string(ukedag) and not val.verify_weekday_number(ukedag) and not ukedag == "exit":
        print(colored("Ugyldig ukedag. Prøv igjen.", "red"))
        ukedag = input("Skriv inn en ukedag: ")
    if ukedag == "exit":
        return

    dbf.print_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag)

def søk_etter_togruter(conn):
    startstasjon = input("Skriv inn startstasjon: ")
    while not val.verify_stasjon(conn, startstasjon) and not startstasjon == "exit":
        print(colored("Ugyldig startstasjon. Prøv igjen.", "red"))
        startstasjon = input("Skriv inn startstasjon: ")
    if startstasjon == "exit":
        return

    endestasjon = input("Skriv inn endestasjon: ")
    while (not val.verify_stasjon(conn, endestasjon) or endestasjon == startstasjon) and not endestasjon == "exit":
        if endestasjon == startstasjon:
            print(colored("Startstasjon og endestasjon kan ikke være like. Prøv igjen.", "red"))
        else:
            print(colored("Ugyldig endestasjon. Prøv igjen.", "red"))
        endestasjon = input("Skriv inn endestasjon: ")
    if endestasjon == "exit":
        return

    dato = input("Skriv inn dato (YYYY-MM-DD): ")
    while not val.verify_date_string(dato) and not dato == "exit":
        print(colored("Ugyldig dato. Prøv igjen.", "red"))
        dato = input("Skriv inn dato (YYYY-MM-DD): ")
    if dato == "exit":
        return

    tid = input("Skriv inn tid (HH:MM): ")
    while not val.verify_time_string(tid) and not tid == "exit":
        print(colored("Ugyldig tid. Prøv igjen.", "red"))
        tid = input("Skriv inn tid (HH:MM): ")
    if tid == "exit":
        return

    dbf.print_togruter_by_stasjoner_and_date(
        conn, startstasjon, endestasjon, dato, tid)

def register_kunde(conn):
    while True:
        navn = input("Skriv inn navn: ")
        if navn == "exit":
            return
        epost = input("Skriv inn email: ")
        if epost == "exit":
            return
        mobilnummer = input("Skriv inn mobilnummer: ")
        while not val.verify_phone_number(mobilnummer) and not mobilnummer == "exit":
            print(colored("Ugyldig mobilnummer. Prøv igjen.", "red"))
            mobilnummer = input("Skriv inn mobilnummer: ")
        if mobilnummer == "exit":
            return
        if (dbf.register_kunde(conn, navn, epost, mobilnummer)):
            print(colored("\nKunde registrert.", 'green'))
            return
        else:
            if (input("\nVil du prøve igjen? y/n ") == "n"):
                return

def bestill_billetter(conn):
    email = input("Skriv inn email: ")
    if email == "exit":
        return
    while not val.verify_user(conn, email) and not email == "exit":
        print(colored("Kunde finnes ikke i systemet. \n", 'red'))
        email = input("Skriv inn email: ")
    if email == "exit":
        return

    print(colored("Kunde verifisert. \n", 'green'))

    print(colored("Søk etter rute: ", 'blue'))
    startstasjon = input("Skriv inn startstasjon: ")
    while not val.verify_stasjon(conn, startstasjon) and not startstasjon == "exit":
        print(colored("Ugyldig startstasjon. Prøv igjen.", "red"))
        startstasjon = input("Skriv inn startstasjon: ")
    if startstasjon == "exit":
        return

    endestasjon = input("Skriv inn endestasjon: ")
    while (not val.verify_stasjon(conn, endestasjon) or endestasjon == startstasjon) and not endestasjon == "exit":
        if endestasjon == startstasjon:
            print(colored("Startstasjon og endestasjon kan ikke være like. Prøv igjen.", "red"))
        else:
            print(colored("Ugyldig endestasjon. Prøv igjen.", "red"))
        endestasjon = input("Skriv inn endestasjon: ")
    if endestasjon == "exit":
        return
    dato = input("Skriv inn dato (YYYY-MM-DD): ")
    while not val.verify_date_string(dato) and not dato == "exit":
        print(colored("Ugyldig dato. Prøv igjen.", "red"))
        dato = input("Skriv inn dato (YYYY-MM-DD): ")
    if dato == "exit":
        return

    togruter = dbf.print_togruter_by_stasjoner_and_date(conn, startstasjon, endestasjon, dato, "00:00")
    if not togruter:
        return

    print(colored("\nVelg rute:", 'blue'))
    select_togrute = input(
        "\nSkriv inn id for ruten du vil kjøpe billettet til: ")
    while not select_togrute.isdigit() or not int(select_togrute) in range(len(togruter)) and not select_togrute == "exit":
        print(colored("Ugyldig id. Prøv igjen.", "red"))
        select_togrute = input(
        "\nSkriv inn id for ruten du vil kjøpe billettet til: ")
    if select_togrute == "exit":
        return
    select_togrute = int(select_togrute)
    togrute_id = togruter[select_togrute][0]
    dato = togruter[select_togrute][6]
    while not val.verify_togrute_id(conn, togrute_id) and not val.verify_togrute_date(conn, togrute_id, dato):
        print(colored("Ugyldig togrute_id. Prøv igjen.", "red"))
        select_togrute = input("\nSkriv inn id for ruten du vil kjøpe billettet til: ")
        while not select_togrute.isdigit() or not int(select_togrute) in range(len(togruter)) and not select_togrute == "exit":
            print(colored("Ugyldig id. Prøv igjen.", "red"))
            select_togrute = input(
            "\nSkriv inn id for ruten du vil kjøpe billettet til: ")
        if select_togrute == "exit":
            return
        select_togrute = int(select_togrute)
        togrute_id = togruter[select_togrute][0]
        dato = togruter[select_togrute][6]

    first = True
    while True:
        seats = dbf.print_available_seats(
            conn, togrute_id, dato, startstasjon, endestasjon)
        if not seats:
            print(colored("Ingen ledige plasser på denne ruten. \n", "red"))
            return
        vogn = input("\nSkriv inn vogn_nummer: ")
        if vogn == "exit":
            return
        plass = input("\nSkriv inn plass_nummer: ")
        if plass == "exit":
            return
        while (not any([int(vogn) == seat[0] and int(plass) == seat[1] for seat in seats])):
            print(
                colored("Plassen er opptatt eller finnes ikke. Prøv igjen.", "red"))
            vogn = input("\nSkriv inn vogn_nummer: ")
            if vogn == "exit":
                return
            plass = input("\nSkriv inn plass_nummer: ")
            if plass == "exit":
                return
        if (vogn == "exit" or plass == "exit"):
            return

        if first:
            ordre_nummer = dbf.create_ordre(
                conn, togrute_id, dato, email, startstasjon, endestasjon)

        plass_type = next((seat[3] for seat in seats if int(
            vogn) == seat[0] and int(plass) == seat[1]))
        if (plass_type == "sove"):
            adjacent_bed_number = 1 if (int(plass) % 2 == 1) else -1

            want_to_buy = input(
                "\nØnsker du å kjøpe den andre sengen i kupeén? (y/n)")
            if (want_to_buy == "y"):
                if not dbf.buy_billett(conn, togrute_id, vogn, str(int(plass) + adjacent_bed_number), ordre_nummer):
                    print(colored("Noe gikk galt. \n", "red"))
                    return
            elif (want_to_buy == "exit"):
                return
        if not dbf.buy_billett(conn, togrute_id, vogn, plass, ordre_nummer):
            print(colored("Noe gikk galt. \n", "red"))
            return
        
        if (input("\nVil du kjøpe flere billeter? (y/n)") != "y"):
            return
        first = False

def vis_dine_fremtidige_reiser(conn):
    epost = input("Skriv inn epost: ")
    if (not val.verify_user(conn, epost)) and not epost == "exit":
        print(colored("Kunde finnes ikke i systemet. \n", "red"))
        epost = input("Skriv inn epost: ")
    if epost == "exit":
        return
    print(colored("Kunde verifisert. \n", "green"))
    dbf.print_orders(conn, epost)