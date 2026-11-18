# meny.py
# Textmenyn och funktionerna som körs för varje menyval.

from kontroller import kontrollera_alla, kontrollera_server
from lagring import (
    GILTIGA_MILJOER,
    exportera_csv,
    filtrera_pa_miljo,
    hitta_server,
    spara_servrar,
)


# Skriver ut servrarna som en tabell med raka kolumner
def skriv_ut_servrar(servrar):
    if not servrar:
        print("Det finns inga servrar att visa.")
        return

    # :<10 betyder vänsterjusterat och 10 tecken brett
    print(f"{'Namn':<10} {'Adress':<15} {'Miljö':<6} {'Roll':<20} {'Status':<8} {'Senast kontrollerad'}")
    print("-" * 82)
    for server in servrar:
        print(
            f"{server['namn']:<10} {server['adress']:<15} {server['miljo']:<6} "
            f"{server['roll']:<20} {server['status']:<8} {server['senast_kontrollerad']}"
        )


# Frågar efter en miljö tills användaren skriver en som finns
def fraga_efter_miljo():
    while True:
        # strip tar bort mellanslag, lower gör om till små bokstäver
        miljo = input("Miljö (dev/test/prod): ").strip().lower()
        if miljo in GILTIGA_MILJOER:
            return miljo
        print("Ogiltig miljö, välj dev, test eller prod.")


# Menyval 2: visa servrar i en miljö
def visa_miljo(servrar):
    miljo = fraga_efter_miljo()
    skriv_ut_servrar(filtrera_pa_miljo(servrar, miljo))


# Menyval 3: lägg till en ny server
def lagg_till_server(servrar, datafil):
    namn = input("Namn: ").strip()

    # Två servrar får inte ha samma namn
    if hitta_server(servrar, namn):
        print(f"Det finns redan en server som heter {namn}.")
        return

    adress = input("Adress: ").strip()
    miljo = fraga_efter_miljo()
    roll = input("Roll: ").strip()

    # En ny server har alltid status unknown och har inte kollats än
    ny_server = {
        "namn": namn,
        "adress": adress,
        "miljo": miljo,
        "roll": roll,
        "status": "unknown",
        "senast_kontrollerad": "",
    }
    servrar.append(ny_server)
    spara_servrar(datafil, servrar)
    print(f"{namn} lades till.")


# Menyval 4: ta bort en server
def ta_bort_server(servrar, datafil):
    namn = input("Namn på servern som ska tas bort: ").strip()
    server = hitta_server(servrar, namn)
    if server is None:
        print(f"Servern {namn} finns inte.")
        return

    # Extra koll innan man tar bort något i produktion
    if server["miljo"] == "prod":
        svar = input(f"{namn} ligger i prod. Är du säker? (j/n): ").strip().lower()
        if svar != "j":
            print("Inget togs bort.")
            return

    servrar.remove(server)
    spara_servrar(datafil, servrar)
    print(f"{namn} togs bort.")


# Menyval 5: kontrollera en server
def kontrollera_en(servrar, datafil):
    namn = input("Namn på servern: ").strip()
    server = hitta_server(servrar, namn)
    if server is None:
        print(f"Servern {namn} finns inte.")
        return

    kontrollera_server(server)
    spara_servrar(datafil, servrar)


# Menyval 6: kontrollera alla servrar
def kontrollera_alla_i_menyn(servrar, datafil):
    kontrollera_alla(servrar)
    spara_servrar(datafil, servrar)


# Menyval 7: exportera rapport
def exportera(servrar):
    filnamn = exportera_csv(servrar)
    print(f"Rapporten sparades i {filnamn}")


# Skriver ut menyvalen
def visa_meny():
    print()
    print("=== Server Inventory Tool ===")
    print("1. Visa alla servrar")
    print("2. Visa servrar i en miljö")
    print("3. Lägg till server")
    print("4. Ta bort server")
    print("5. Kontrollera en server")
    print("6. Kontrollera alla servrar")
    print("7. Exportera rapport (CSV)")
    print("0. Avsluta")


# Själva menyn, körs i en loop tills man väljer 0
def kor_meny(servrar, datafil):
    while True:
        visa_meny()
        val = input("Välj: ").strip()

        if val == "1":
            skriv_ut_servrar(servrar)
        elif val == "2":
            visa_miljo(servrar)
        elif val == "3":
            lagg_till_server(servrar, datafil)
        elif val == "4":
            ta_bort_server(servrar, datafil)
        elif val == "5":
            kontrollera_en(servrar, datafil)
        elif val == "6":
            kontrollera_alla_i_menyn(servrar, datafil)
        elif val == "7":
            exportera(servrar)
        elif val == "0":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val, skriv en siffra mellan 0 och 7.")
