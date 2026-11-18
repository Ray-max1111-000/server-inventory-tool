# lagring.py
# Här finns allt som har med filer att göra: läsa och spara JSON
# och exportera rapporter som CSV.

import csv
import json
import os
from datetime import datetime
from pathlib import Path

# Miljöer som är tillåtna
GILTIGA_MILJOER = ["dev", "test", "prod"]

# Kolumnerna i CSV-rapporten
FALT = ["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"]


# Tar reda på vilken fil servrarna ska sparas i
def hamta_datafil():
    # Om INVENTORY_DATAFIL inte är satt används servrar.json
    filnamn = os.environ.get("INVENTORY_DATAFIL", "servrar.json")
    return Path(filnamn)


# Läser in servrarna från JSON-filen
def las_servrar(datafil):
    # Finns inte filen börjar vi med en tom lista i stället för att krascha
    if not datafil.exists():
        return []

    with open(datafil, "r", encoding="utf-8") as fil:
        return json.load(fil)


# Sparar servrarna till JSON-filen
def spara_servrar(datafil, servrar):
    # indent=2 gör filen lätt att läsa, ensure_ascii=False behåller å, ä, ö
    with open(datafil, "w", encoding="utf-8") as fil:
        json.dump(servrar, fil, indent=2, ensure_ascii=False)


# Letar upp en server med ett visst namn, ger None om den inte finns
def hitta_server(servrar, namn):
    for server in servrar:
        if server["namn"] == namn:
            return server
    return None


# Ger en ny lista med bara servrarna i en viss miljö
def filtrera_pa_miljo(servrar, miljo):
    resultat = []
    for server in servrar:
        if server["miljo"] == miljo:
            resultat.append(server)
    return resultat


# Skriver alla servrar till en CSV-fil i mappen rapporter/
def exportera_csv(servrar):
    # Skapar mappen om den inte redan finns
    katalog = Path("rapporter")
    katalog.mkdir(exist_ok=True)

    # Datum och tid i filnamnet, t.ex. inventering_2026-11-18_1422.csv
    tidpunkt = datetime.now().strftime("%Y-%m-%d_%H%M")
    filnamn = katalog / f"inventering_{tidpunkt}.csv"

    with open(filnamn, "w", newline="", encoding="utf-8") as fil:
        skrivare = csv.DictWriter(fil, fieldnames=FALT)
        skrivare.writeheader()  # rubrikraden
        skrivare.writerows(servrar)  # en rad per server

    return filnamn
