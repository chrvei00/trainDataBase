import util.database_functions as dbf
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


        valg = int(input("\nVelg handling (0-5): "))
        print("\n-----------------------------------------\n")

        #Finn togruter for en stasjon på en ukedag
        if valg == 1:
            stasjon = input("Skriv inn stasjon: ")
            ukedag = input("Skriv inn ukedag (0-6, hvor 0 er mandag): ")
            togruter = dbf.print_togruter_by_stasjon_and_ukedag(conn, stasjon, ukedag)            
        elif valg == 2:
            startstasjon = input("Skriv inn startstasjon: ")
            endestasjon = input("Skriv inn endestasjon: ")
            dato = input("Skriv inn dato (YYYY-MM-DD): ")
            tid = input("Skriv inn tid (HH:MM): ")
            dbf.print_togruter_by_stasjoner_and_date(conn, startstasjon, endestasjon, dato)

        #Registrer kunde
        elif valg == 3:
            while True:
                navn = input("Skriv inn navn: ")
                epost = input("Skriv inn epost: ")
                mobilnummer = input("Skriv inn mobilnummer: ")
                if(dbf.register_kunde(conn, navn, epost, mobilnummer)):
                    break
                else:
                    if(input("\nVil du prøve igjen? y/n") == "n"):
                        break
                    
        elif valg == 4:
            navn = input("Skriv inn navn: ")
            mobilnummer = input("Skriv inn mobilnummer: ")
            if (not utils.verify_user(conn, navn, mobilnummer)):
                print("Kunde finnes ikke i systemet. \n")
                break
            print("Kunde verifisert. \n")
            startstasjon = input("Skriv inn startstasjon: ")
            endestasjon = input("Skriv inn endestasjon: ")

            togrute = utils.find_togrute(conn, startstasjon, endestasjon)
            if not togrute:
                print(f"Fant ingen togruter fra {startstasjon} til {endestasjon}\n")
                break
            
            dato = input("Skriv inn dato (YYYY-MM-DD): ")

            #TODO print billeter (med plassnummer)
            while True:
                billett = input("Skriv inn billett: ")
                #TODO dbf.buy_billett(conn, billett)
                #TODO print billett
                print("Billett kjøpt. \n")
                if(input("Vil du kjøpe flere billeter? (y/n)") == "n"):
                    break
        elif valg == 5:
            navn = input("Skriv inn navn: ")
            mobilnummer = input("Skriv inn mobilnummer: ")
            if (not utils.verify_user(conn, navn, mobilnummer)):
                print("Kunde finnes ikke i systemet. \n")
                break
            print("Kunde verifisert. \n")
            dbf.print_orders(conn, navn, mobilnummer)
        elif valg == 0:
            break
        else:
            print("Ugyldig valg. Prøv igjen.")

        print("\n-----------------------------------------\n")
        if(input("\nVil du utføre en ny handling? (y/n)") == "n"):
            break
