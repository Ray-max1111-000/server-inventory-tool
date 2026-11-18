# kontroller.py
# Kollar om servrar svarar på ping.

import subprocess
from datetime import datetime


# Pingar en adress en gång, ger True om den svarar
def svarar_pa_ping(adress):
    # Kommandot skickas som en lista, då behövs inget shell
    # -c 1 betyder att bara ett paket skickas
    kommando = ["ping", "-c", "1", adress]

    try:
        # capture_output gör att ping-texten inte skrivs ut i terminalen
        resultat = subprocess.run(kommando, capture_output=True, timeout=5)
    except subprocess.TimeoutExpired:
        # Svarar servern inte inom 5 sekunder räknas den som nere
        return False

    # Exitkod 0 betyder att ping fick svar
    return resultat.returncode == 0


# Kollar en server och uppdaterar status och tid
def kontrollera_server(server):
    if svarar_pa_ping(server["adress"]):
        server["status"] = "up"
    else:
        server["status"] = "down"

    # Sparar när servern kollades, t.ex. 2026-11-18 14:22
    server["senast_kontrollerad"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"{server['namn']:<10} {server['adress']:<15} {server['status']}")

    return server["status"] == "up"


# Kollar alla servrar i listan
def kontrollera_alla(servrar):
    # Returnerar True bara om alla servrar svarade
    alla_uppe = True
    for server in servrar:
        if not kontrollera_server(server):
            alla_uppe = False
    return alla_uppe
