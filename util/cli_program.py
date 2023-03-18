import util.database_methods as dbm
import util.utils as utils

def start(conn):
    while True:
        print("\n=========================================\n")
        print("Velg en handling:")
        print("1. Hent togruter for en stasjon på en ukedag")
        print("2. Søk etter togruter")
        print("3. Registrer kunde")
        print("4. Bestill billeter")
        print("5. Vis ordre")
        print("0. Avslutt")


        valg = int(input("Velg handling (0-5): "))


        if valg == 1:
            stasjon = input("Skriv inn stasjon: ")
            ukedag = input("Skriv inn ukedag (0-6, hvor 0 er søndag): ")
            # TODO : finn togruter
            # togruter = dbm.get_togruter(conn, stasjon, ukedag)
            print("\nTogruter for stasjonen", stasjon, "på ukedag", ukedag, ":")
            for togrute in []:
                print(togrute)
        elif valg == 2:
            start_stasjon = input("Skriv inn startstasjon: ")
            ende_stasjon = input("Skriv inn endestasjon: ")
            dato = input("Skriv inn dato (YYYY-MM-DD): ")
            tid = input("Skriv inn tid (HH:MM): ")
            # TODO : finn togruter
            # togruter = dbm.get_togruter(conn, stasjon, ukedag)
            print("\nSøker etter togruter fra", start_stasjon, "til", ende_stasjon, "på", dato, "kl", tid)
        #Registrer kunde
        elif valg == 3:
            navn = input("Skriv inn navn: ")
            epost = input("Skriv inn epost: ")
            mobilnummer = input("Skriv inn mobilnummer: ")
            dbm.register_kunde(conn, navn, epost, mobilnummer)
        elif valg == 4:
            navn = input("Skriv inn navn: ")
            mobilnummer = input("Skriv inn mobilnummer: ")
            #TODO util.verify_user(conn, navn, mobilnummer)
            print("Kunde verifisert. \n")
            togrute = input("Skriv inn togrute: ")
            #TODO dbm.get_togrute(conn, togrute)
            #TODO print stasjoner på togrute
            start_stasjon = input("Skriv inn startstasjon: ")
            ende_stasjon = input("Skriv inn endestasjon: ")
            #TODO util.verify_stasjoner(conn, togrute, start_stasjon, ende_stasjon)
            #TODO print billeter (med plassnummer)
            while True:
                billett = input("Skriv inn billett: ")
                #TODO dbm.buy_billett(conn, billett)
                #TODO print billett
                print("Billett kjøpt. \n")
                if(input("Vil du kjøpe flere billeter? (y/n)") == "n"):
                    break
        elif valg == 5:
            navn = input("Skriv inn navn: ")
            mobilnummer = input("Skriv inn mobilnummer: ")
            #TODO util.verify_user(conn, navn, mobilnummer)
            print("Kunde verifisert. \n")
            #TODO dbm.get_orders(conn, navn, mobilnummer)
            #TODO print ordre
        elif valg == 0:
            break
        else:
            print("Ugyldig valg. Prøv igjen.")

        if(input("Vil du utføre en ny handling? (y/n)") == "n"):
            break
