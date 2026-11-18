# main.py
# Startpunkt för programmet. Utan argument startar menyn,
# annars körs det som ett vanligt kommandoradsverktyg.

import argparse
import sys

from kontroller import kontrollera_alla, kontrollera_server
from lagring import (
    GILTIGA_MILJOER,
    exportera_csv,
    filtrera_pa_miljo,
    hamta_datafil,
    hitta_server,
    las_servrar,
    spara_servrar,
)
from meny import kor_meny, skriv_ut_servrar


# Bestämmer vilka flaggor programmet tar emot
def las_argument():
    parser = argparse.ArgumentParser(
        description="Håller koll på servrar och kollar om de svarar på ping. "
        "Utan argument startar en textmeny."
    )
    # store_true betyder att flaggan blir True om den skrivs med
    parser.add_argument("--lista", action="store_true", help="visa alla servrar")
    # choices gör att bara dev, test och prod godkänns
    parser.add_argument("--miljo", choices=GILTIGA_MILJOER, help="visa bara servrar i en miljö (används med --lista)")
    parser.add_argument("--kontrollera", metavar="NAMN", help="kontrollera en server")
    parser.add_argument("--kontrollera-alla", action="store_true", help="kontrollera alla servrar")
    parser.add_argument("--export", action="store_true", help="exportera en CSV-rapport till rapporter/")
    return parser.parse_args()


def main():
    args = las_argument()
    datafil = hamta_datafil()
    servrar = las_servrar(datafil)

    # --lista, med eller utan --miljo
    if args.lista:
        if args.miljo:
            skriv_ut_servrar(filtrera_pa_miljo(servrar, args.miljo))
        else:
            skriv_ut_servrar(servrar)

    # --kontrollera NAMN
    elif args.kontrollera:
        server = hitta_server(servrar, args.kontrollera)
        if server is None:
            print(f"Servern {args.kontrollera} finns inte.")
            sys.exit(1)

        uppe = kontrollera_server(server)
        spara_servrar(datafil, servrar)
        # Exitkod 1 om servern är nere
        if not uppe:
            sys.exit(1)

    # --kontrollera-alla
    elif args.kontrollera_alla:
        alla_uppe = kontrollera_alla(servrar)
        spara_servrar(datafil, servrar)
        # Exitkod 1 om minst en server är nere
        if not alla_uppe:
            sys.exit(1)

    # --export
    elif args.export:
        filnamn = exportera_csv(servrar)
        print(f"Rapporten sparades i {filnamn}")

    # Inga argument, starta menyn
    else:
        kor_meny(servrar, datafil)

    # Allt gick bra
    sys.exit(0)


# Kör bara main() när filen startas direkt
if __name__ == "__main__":
    main()
