import util.database_functions as dbf
import util.utils as utils
import util.validation as val

def start(conn):
    while True:
        print("\n=========================================\n")
        print("Velg en handling:")
        print("1. Hent togruter for en stasjon på en ukedag")
        print("2. Søk etter togruter")
        print("3. Registrer kunde")
        print("4. Bestill billeter")
        print("5. Vis dine fremtidige reiser")
        print("0. Avslutt")


        valg = int(input("\nVelg handling (0-5): "))
        print("\n-----------------------------------------\n")

        #Finn togruter for en stasjon på en ukedag
        if valg == 1:
            stasjon = input("Skriv inn stasjon: ")
            while not val.verify_stasjon(conn, stasjon):
                print("Ugyldig stasjon. Prøv igjen.")
                stasjon = input("Skriv inn stasjon: ")

            ukedag = input("Skriv inn ukedag: ")
            while not utils.is_valid_weekday_string(ukedag) and not utils.is_valid_weekday_number(ukedag):
                print("Ugyldig ukedag. Prøv igjen.")
                ukedag = input("Skriv inn en ukedag: ")

            dbf.print_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag)            
        elif valg == 2:
            startstasjon = input("Skriv inn startstasjon: ")
            while not val.verify_stasjon(conn, startstasjon):
                print("Ugyldig startstasjon. Prøv igjen.")
                stasjon = input("Skriv inn startstasjon: ")

            endestasjon = input("Skriv inn endestasjon: ")
            while not val.verify_stasjon(conn, endestasjon):
                print("Ugyldig endestasjon. Prøv igjen.")
                stasjon = input("Skriv inn endestasjon: ")

            dato = input("Skriv inn dato (YYYY-MM-DD): ")
            while not utils.is_valid_date_string(dato):
                print("Ugyldig dato. Prøv igjen.")
                dato = input("Skriv inn dato (YYYY-MM-DD): ")

            tid = input("Skriv inn tid (HH:MM): ")
            while not utils.is_valid_time_string(tid):
                print("Ugyldig tid. Prøv igjen.")
                tid = input("Skriv inn tid (HH:MM): ")

            dbf.print_togruter_by_stasjoner_and_date(conn, startstasjon, endestasjon, dato, tid)

        #Registrer kunde
        elif valg == 3:
            while True:
                navn = input("Skriv inn navn: ")
                epost = input("Skriv inn email: ")
                mobilnummer = input("Skriv inn mobilnummer: ")
                if(dbf.register_kunde(conn, navn, epost, mobilnummer)):
                    break
                else:
                    if(input("\nVil du prøve igjen? y/n") == "n"):
                        break
                    
        elif valg == 4:
            navn = input("Skriv inn navn: ")
            email = input("Skriv inn email: ")
            if (not val.verify_user(conn, email)):
                print("Kunde finnes ikke i systemet. \n")
                break
            print("Kunde verifisert. \n")

            startstasjon = input("Skriv inn startstasjon: ")
            while not val.verify_stasjon(conn, startstasjon):
                print("Ugyldig startstasjon. Prøv igjen.")
                stasjon = input("Skriv inn startstasjon: ")

            endestasjon = input("Skriv inn endestasjon: ")
            while not val.verify_stasjon(conn, endestasjon):
                print("Ugyldig endestasjon. Prøv igjen.")
                stasjon = input("Skriv inn endestasjon: ")
            
            dato = input("Skriv inn dato (YYYY-MM-DD): ")
            while not utils.is_valid_date_string(dato):
                print("Ugyldig dato. Prøv igjen.")
                dato = input("Skriv inn dato (YYYY-MM-DD): ")

            if not dbf.print_togruter_by_stasjoner_and_date(conn, startstasjon, endestasjon, dato, "00:00"):
                break

            togrute_id = input("Skriv inn id for ruten du vil kjøpe billettet til: ")
            
            first = True
            while True:
                seats = dbf.print_available_seats(conn, togrute_id, dato, startstasjon, endestasjon)
                vogn = input("\nSkriv inn vogn_nummer (eller none): ")
                if vogn == "none":
                    break
                plass = input("\nSkriv inn plass_nummer (eller none): ")
                if plass == "none":
                    break
                while (not any([int(plass) == seat[0] and int(vogn) == seat[1] for seat in seats])):
                    print("Plassen er opptatt eller finnes ikke. Prøv igjen.")
                    vogn = input("\nSkriv inn vogn_nummer (eller none): ")
                    if vogn == "none":
                        break
                    plass = input("\nSkriv inn plass_nummer (eller none): ")
                    if plass == "none":
                        break
                if (vogn == "none" or plass == "none"):
                    break
                if first:
                    print("Lager ordre...")
                    ordre_nummer = dbf.create_ordre(conn, togrute_id, dato, navn, email, startstasjon, endestasjon)
                if not dbf.buy_billett(conn, togrute_id, vogn, plass, ordre_nummer):
                    break
                if(input("\nVil du kjøpe flere billeter? (y/n)") == "n"):
                    break
                first = False

        elif valg == 5:
            epost = val("Skriv inn epost: ")
            if (not val.verify_user(conn, epost)):
                print("Kunde finnes ikke i systemet. \n")
                break
            print("Kunde verifisert. \n")
            dbf.print_orders(conn, epost)
        elif valg == 0:
            break
        else:
            print("Ugyldig valg. Prøv igjen.")

        print("\n-----------------------------------------\n")
        if(input("\nVil du utføre en ny handling? (y/n)") == "n"):
            break
