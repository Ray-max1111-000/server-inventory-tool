# Server Inventory Tool

Ett litet program i Python för att hålla koll på servrar. Man kan spara servrar med namn, adress, miljö och roll, kolla om de svarar på ping och göra en rapport som CSV.

Programmet kan användas på två sätt:

- med en **textmeny** där man väljer med siffror
- direkt från **kommandoraden** med flaggor, t.ex. `--lista` eller `--kontrollera-alla`

## Vad programmet gör

- Visar alla servrar i en tabell
- Visar bara servrar i en viss miljö (`dev`, `test` eller `prod`)
- Lägger till nya servrar (de får alltid status `unknown`)
- Tar bort servrar (frågar en extra gång om servern ligger i `prod`)
- Kollar om en server eller alla servrar svarar på ping
- Sparar status (`up`/`down`) och när servern kontrollerades senast
- Exporterar alla servrar till en CSV-fil i mappen `rapporter/`

Allt sparas i en JSON-fil så att servrarna finns kvar nästa gång man startar programmet.

## Vad som behövs

- Python 3.8 eller nyare
- Linux eller macOS (kommandot `ping -c` finns inte på Windows, där kan man använda WSL eller kursens container)
- Inga extra paket behöver installeras, programmet använder bara standardbiblioteket

## Komma igång

Klona repot och gå in i mappen:

```bash
git clone <länk till repot>
cd service-inventory-tool
```

Det finns redan en `servrar.json` med fyra servrar att testa med.

## Starta med textmenyn

Kör programmet utan argument:

```bash
python3 main.py
```

Då visas menyn:

```text
=== Server Inventory Tool ===
1. Visa alla servrar
2. Visa servrar i en miljö
3. Lägg till server
4. Ta bort server
5. Kontrollera en server
6. Kontrollera alla servrar
7. Exportera rapport (CSV)
0. Avsluta
```

Skriv siffran för det du vill göra och tryck Enter. Menyn kommer tillbaka efter varje val tills du väljer `0`.

Några saker att veta:

- Skriver man ett val som inte finns får man ett meddelande och menyn visas igen.
- När man lägger till en server måste miljön vara `dev`, `test` eller `prod`. Annars frågar programmet igen.
- Två servrar kan inte ha samma namn.
- Om man skriver namnet på en server som inte finns säger programmet till.

## Starta från kommandoraden

| Kommando | Vad som händer |
|---|---|
| `python3 main.py --help` | Visar hjälptexten |
| `python3 main.py --lista` | Skriver ut alla servrar |
| `python3 main.py --lista --miljo prod` | Skriver bara ut servrar i `prod` |
| `python3 main.py --kontrollera web01` | Kollar servern `web01` |
| `python3 main.py --kontrollera-alla` | Kollar alla servrar |
| `python3 main.py --export` | Skapar en CSV-rapport i `rapporter/` |

### Exitkoder

Programmet avslutas med en exitkod så att det går att använda i skript:

| Exitkod | Betyder |
|---|---|
| `0` | Allt gick bra |
| `1` | Minst en server är nere efter `--kontrollera` eller `--kontrollera-alla`, eller servern man angav finns inte |

Man kan se exitkoden direkt efter körningen:

```bash
python3 main.py --kontrollera-alla
echo $?
```

Tips: `test01` har adressen `192.0.2.10` som inte finns på riktigt, så `--kontrollera-alla` ger alltid exitkod `1` med startdatan.

## Miljövariabeln INVENTORY_DATAFIL

Programmet läser vilken datafil det ska använda från miljövariabeln `INVENTORY_DATAFIL`. Är den inte satt används `servrar.json`.

Använda en annan fil för en körning:

```bash
INVENTORY_DATAFIL=mina_servrar.json python3 main.py --lista
```

Eller sätta den för hela terminalen:

```bash
export INVENTORY_DATAFIL=mina_servrar.json
python3 main.py
```

Om filen inte finns startar programmet med en tom lista. Filen skapas när man lägger till första servern.

## CSV-rapporten

`--export` (eller val 7 i menyn) sparar en fil i mappen `rapporter/`. Mappen skapas automatiskt om den inte finns. Filnamnet har datum och tid, till exempel:

```text
rapporter/inventering_2026-11-18_1422.csv
```

Filen har en rubrikrad och sedan en rad per server:

```text
namn,adress,miljo,roll,status,senast_kontrollerad
web01,example.com,prod,webbserver,up,2026-11-18 14:22
```

Mappen `rapporter/` ligger i `.gitignore` så rapporterna hamnar inte i git.

## Hur en server ser ut

Varje server är en dictionary i en lista:

```json
{
  "namn": "web01",
  "adress": "example.com",
  "miljo": "prod",
  "roll": "webbserver",
  "status": "unknown",
  "senast_kontrollerad": ""
}
```

- `miljo` kan vara `dev`, `test` eller `prod`
- `status` kan vara `up`, `down` eller `unknown`
- `senast_kontrollerad` har formatet `ÅÅÅÅ-MM-DD TT:MM`, eller är tom om servern inte har kollats än

## Hur projektet är uppbyggt

```text
service-inventory-tool/
├── main.py          startpunkt, läser argument med argparse
├── meny.py          textmenyn och funktionerna för varje val
├── lagring.py       läser/sparar JSON, exporterar CSV, söker och filtrerar
├── kontroller.py    pingar servrar och uppdaterar status
├── servrar.json     startdata
├── .gitignore
├── README.md
└── REDOGORELSE.md
```

| Fil | Ansvar |
|---|---|
| `main.py` | Läser argumenten. Utan argument startas menyn, annars körs rätt kommando och programmet avslutas med rätt exitkod. |
| `meny.py` | Menyn i en loop och allt som frågar användaren om något med `input()`. Här finns också utskriften av tabellen. |
| `lagring.py` | Allt som har med filer och data att göra: läsa och spara JSON, exportera CSV, hitta en server på namn och filtrera på miljö. |
| `kontroller.py` | Kör `ping` med `subprocess` och uppdaterar `status` och `senast_kontrollerad`. |

Menyn och kommandoraden använder samma funktioner i `lagring.py` och `kontroller.py`. Koden för att kolla en server finns alltså bara på ett ställe.

## Om ping

Vissa nätverk (t.ex. skol- eller jobbnätverk) blockerar ping mot internet. Då kan `example.com` visas som `down` fast koden fungerar. `127.0.0.1` och `localhost` är den egna datorn och svarar alltid.

Varje ping får max 5 sekunder på sig. Svarar servern inte på den tiden räknas den som `down`.
