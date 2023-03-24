import util.database_functions as dbf
import util.validation as val
from termcolor import colored

def start(conn):
    while True:
        print(colored("\n=========================================\n", "magenta"))
        print(colored("Velg en handling:", "blue"))
        print("1. Hent togruter for en stasjon på en ukedag")
        print("2. Søk etter togruter")
        print("3. Registrer kunde")
        print("4. Bestill billeter")
        print("5. Vis dine fremtidige reiser")
        print("0. Avslutt")


        valg = int(input("\nVelg handling (0-5): "))
        print(colored("\n-----------------------------------------\n", "magenta"))

        #Finn togruter for en stasjon på en ukedag
        if valg == 1:
            stasjon = input("Skriv inn stasjon: ")
            while not val.verify_stasjon(conn, stasjon):
                print(colored("Ugyldig stasjon. Prøv igjen.", "red"))
                stasjon = input("Skriv inn stasjon: ")

            ukedag = input("Skriv inn ukedag: ")
            while not val.verify_weekday_string(ukedag) and not val.verify_weekday_number(ukedag):
                print(colored("Ugyldig ukedag. Prøv igjen.", "red"))
                ukedag = input("Skriv inn en ukedag: ")

            dbf.print_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag)            
        elif valg == 2:
            startstasjon = input("Skriv inn startstasjon: ")
            while not val.verify_stasjon(conn, startstasjon):
                print(colored("Ugyldig startstasjon. Prøv igjen.", "red"))
                startstasjon = input("Skriv inn startstasjon: ")

            endestasjon = input("Skriv inn endestasjon: ")
            while not val.verify_stasjon(conn, endestasjon):
                print(colored("Ugyldig endestasjon. Prøv igjen.", "red"))
                endestasjon = input("Skriv inn endestasjon: ")

            dato = input("Skriv inn dato (YYYY-MM-DD): ")
            while not val.verify_date_string(dato):
                print(colored("Ugyldig dato. Prøv igjen.", "red"))
                dato = input("Skriv inn dato (YYYY-MM-DD): ")

            tid = input("Skriv inn tid (HH:MM): ")
            while not val.verify_time_string(tid):
                print(colored("Ugyldig tid. Prøv igjen.", "red"))
                tid = input("Skriv inn tid (HH:MM): ")

            dbf.print_togruter_by_stasjoner_and_date(conn, startstasjon, endestasjon, dato, tid)

        #Registrer kunde
        elif valg == 3:
            while True:
                navn = input("Skriv inn navn: ")
                epost = input("Skriv inn email: ")
                mobilnummer = input("Skriv inn mobilnummer: ")
                if(dbf.register_kunde(conn, navn, epost, mobilnummer)):
                    print(colored("\nKunde registrert.", 'green'))
                    break
                else:
                    if(input("\nVil du prøve igjen? y/n") == "n"):
                        break
                    
        elif valg == 4:
            email = input("Skriv inn email: ")
            while not val.verify_user(conn, email):
                print(colored("Kunde finnes ikke i systemet. \n", 'red'))
                email = input("Skriv inn email: ")

            print(colored("Kunde verifisert. \n", 'green'))

            print(colored("Søk etter rute: ", 'blue'))
            startstasjon = input("Skriv inn startstasjon: ")
            while not val.verify_stasjon(conn, startstasjon):
                print(colored("Ugyldig startstasjon. Prøv igjen.", "red"))
                startstasjon = input("Skriv inn startstasjon: ")

            endestasjon = input("Skriv inn endestasjon: ")
            while not val.verify_stasjon(conn, endestasjon):
                print(colored("Ugyldig endestasjon. Prøv igjen.", "red"))
                endestasjon = input("Skriv inn endestasjon: ")
            
            dato = input("Skriv inn dato (YYYY-MM-DD): ")
            while not val.verify_date_string(dato):
                print(colored("Ugyldig dato. Prøv igjen.", "red"))
                dato = input("Skriv inn dato (YYYY-MM-DD): ")

            if not dbf.print_togruter_by_stasjoner_and_date(conn, startstasjon, endestasjon, dato, "00:00"):
                break

            print(colored("\nVelg rute:", 'blue'))
            togrute_id = input("\nSkriv inn id for ruten du vil kjøpe billettet til: ")
            while not val.verify_togrute_id(conn, togrute_id):
                print(colored("Ugyldig togrute_id. Prøv igjen.", "red"))
                togrute_id = input("Skriv inn id for ruten du vil kjøpe billettet til: ")
                
            dato = input("Skriv inn dato for toget du ønsker (YYYY-MM-DD): ")
            while not val.verify_date_string(dato) or not val.verify_togruteforekomst_exists(conn, dato, togrute_id):
                print(colored("Ugyldig dato eller format. Prøv igjen.", "red"))
                dato = input("Skriv inn dato for toget du ønsker (YYYY-MM-DD): ")
            
            first = True
            while True:
                seats = dbf.print_available_seats(conn, togrute_id, dato, startstasjon, endestasjon)
                if not seats:
                    print(colored("Ingen ledige plasser på denne ruten. \n", "red"))
                    break
                vogn = input("\nSkriv inn vogn_nummer (eller none): ")
                if vogn == "none":
                    break
                plass = input("\nSkriv inn plass_nummer (eller none): ")
                if plass == "none":
                    break
                while (not any([int(vogn) == seat[0] and int(plass) == seat[1] for seat in seats])):
                    print(colored("Plassen er opptatt eller finnes ikke. Prøv igjen.", "red"))
                    vogn = input("\nSkriv inn vogn_nummer (eller none): ")
                    if vogn == "none":
                        break
                    plass = input("\nSkriv inn plass_nummer (eller none): ")
                    if plass == "none":
                        break
                if (vogn == "none" or plass == "none"):
                    break
                if first:
                    ordre_nummer = dbf.create_ordre(conn, togrute_id, dato, email, startstasjon, endestasjon)
                if not dbf.buy_billett(conn, togrute_id, vogn, plass, ordre_nummer):
                    break
                if(input("\nVil du kjøpe flere billeter? (y/n)") == "n"):
                    break
                first = False

        elif valg == 5:
            epost = input("Skriv inn epost: ")
            if (not val.verify_user(conn, epost)):
                print(colored("Kunde finnes ikke i systemet. \n", "red"))
                break
            print(colored("Kunde verifisert. \n", "green"))
            dbf.print_orders(conn, epost)
        elif valg == 0:
            break
        else:
            print(colored("Ugyldig valg. Prøv igjen.", "red"))

        print(colored("\n-----------------------------------------\n", "magenta"))
        if(input("\nVil du utføre en ny handling? (y/n)") == "n"):
            break
