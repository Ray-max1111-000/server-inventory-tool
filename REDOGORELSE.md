# Redogörelse

## 1. Tre konstruktioner i koden

**Villkor (if/elif/else) i `meny.py`, funktionen `kor_meny`**

```python
if val == "1":
    skriv_ut_servrar(servrar)
elif val == "2":
    visa_miljo(servrar)
...
else:
    print("Ogiltigt val, skriv en siffra mellan 0 och 7.")
```

Python kollar villkoren uppifrån och ner och kör bara det första som är sant. `elif` betyder "annars om". Om inget av valen stämmer hamnar man i `else` och får ett felmeddelande. Indraget (fyra mellanslag) visar vilken kod som hör till vilket villkor. Jag jämför med strängar som `"1"` eftersom `input()` alltid ger en sträng, så jag slipper göra om svaret till ett tal och riskera att programmet kraschar om någon skriver bokstäver.

**While-loop i `meny.py`, funktionen `fraga_efter_miljo`**

```python
while True:
    miljo = input("Miljö (dev/test/prod): ").strip().lower()
    if miljo in GILTIGA_MILJOER:
        return miljo
    print("Ogiltig miljö, välj dev, test eller prod.")
```

`while True` är en loop som snurrar för alltid tills något stoppar den. Här stoppas den av `return`, som både avslutar loopen och skickar tillbaka värdet. `in` kollar om det användaren skrev finns i listan med giltiga miljöer. `.strip()` tar bort mellanslag i början och slutet och `.lower()` gör om till små bokstäver, så `PROD ` fungerar också. Så länge användaren skriver fel frågar programmet igen, vilket är det som krävs i G3.

**Funktion med parametrar och return i `lagring.py`, funktionen `hitta_server`**

```python
def hitta_server(servrar, namn):
    for server in servrar:
        if server["namn"] == namn:
            return server
    return None
```

Funktionen tar emot listan och namnet som parametrar, så den behöver inga globala variabler. En `for`-loop går igenom servrarna en i taget. Hittar den rätt namn skickas den servern tillbaka direkt med `return`. Annars returneras `None`, som betyder "ingenting". Den används på flera ställen: när man lägger till (för att stoppa dubletter), tar bort och kontrollerar en server, både i menyn och i `main.py`.

## 2. Varför en lista med dictionaries?

En server har flera egenskaper som hör ihop (namn, adress, miljö osv.). En dictionary passar bra för det, eftersom man kommer åt värdena med ett tydligt namn, t.ex. `server["status"]` i stället för `server[4]`. Alla servrar ligger sedan i en lista, eftersom vi har många servrar, och en lista går lätt att loopa igenom, lägga till i med `append()` och ta bort från med `remove()` (se `lagg_till_server` och `ta_bort_server` i `meny.py`).

Ett annat stort plus är att en lista med dictionaries ser ut precis som JSON-filen. Därför kan `json.load()` och `json.dump()` i `lagring.py` läsa och spara den direkt, och `csv.DictWriter` i `exportera_csv` kan skriva den rakt av.

Alla värden i en server är strängar (`str`): namn, adress, miljö, roll, status och även `senast_kontrollerad` som är en text med datum och tid, t.ex. `"2026-11-18 14:22"`. Om servern inte har kontrollerats är det en tom sträng `""`.

## 3. Varför JSON för data men CSV för rapporten?

JSON används för datan som programmet själv läser och skriver (`las_servrar` och `spara_servrar` i `lagring.py`). JSON kan spara listor och dictionaries som de är, så när programmet läser filen får vi tillbaka exakt samma struktur. Det är också lätt att läsa för en människa.

CSV används för rapporten (`exportera_csv` i `lagring.py`) eftersom den är tänkt för någon annan, t.ex. en chef eller kollega. En CSV-fil kan öppnas direkt i Excel eller Google Sheets och blir en vanlig tabell. CSV är platt (rader och kolumner) och passar bra för en rapport, men sämre för att lagra data med nästlade strukturer. Därför används olika format till olika saker.

## 4. Hur programmet är uppdelat

Programmet är uppdelat i fyra filer där varje fil har ett eget ansvar:

- **`main.py`** är startpunkten. Funktionen `las_argument` sätter upp `argparse` och `main` bestämmer vad som ska hända. Utan argument anropas `kor_meny` i `meny.py`. Längst ner finns `if __name__ == "__main__":` så att `main()` bara körs när filen startas direkt.
- **`meny.py`** innehåller allt som pratar med användaren via `input()`. Varje menyval har en egen funktion, t.ex. `lagg_till_server` och `ta_bort_server`. Här finns också `skriv_ut_servrar` som skriver tabellen, och den används även av `main.py` för `--lista`.
- **`lagring.py`** sköter filer och data: `hamta_datafil`, `las_servrar`, `spara_servrar`, `exportera_csv` och hjälpfunktionerna `hitta_server` och `filtrera_pa_miljo`.
- **`kontroller.py`** kör ping. `svarar_pa_ping` kör själva kommandot, `kontrollera_server` uppdaterar en server och `kontrollera_alla` loopar över alla.

Det viktiga är att menyn och kommandoraden använder samma funktioner. Både `kontrollera_en` i `meny.py` och `--kontrollera` i `main.py` anropar `kontrollera_server`, så logiken finns bara på ett ställe.

## 5. Moduler från standardbiblioteket

- **`json`** (`lagring.py`) för att läsa och spara servrarna i `servrar.json`.
- **`csv`** (`lagring.py`) för att skriva rapporten med `DictWriter`, som även skriver rubrikraden.
- **`os`** (`lagring.py`) för att läsa miljövariabeln `INVENTORY_DATAFIL` med `os.environ.get()`, där andra argumentet är standardvärdet.
- **`pathlib`** (`lagring.py`) för `Path`. Jag använder `exists()` för att kolla om datafilen finns och `mkdir(exist_ok=True)` för att skapa `rapporter/`. Med `/` kan man sätta ihop sökvägar på ett enkelt sätt.
- **`datetime`** (`lagring.py` och `kontroller.py`) för att få aktuell tid. `strftime` gör om tiden till text, t.ex. `"%Y-%m-%d %H:%M"` för `senast_kontrollerad`.
- **`subprocess`** (`kontroller.py`) för att köra `ping` med `subprocess.run()`. Exitkoden i `returncode` säger om servern svarade.
- **`argparse`** (`main.py`) för flaggorna på kommandoraden. Den skapar `--help` automatiskt och `choices` gör att `--miljo` bara tar emot giltiga miljöer.
- **`sys`** (`main.py`) för `sys.exit()` så att programmet avslutas med exitkod 0 eller 1.

## 6. Tre exempel på god praxis

**Ingen kopierad logik.** Koden för att kolla en server finns bara i `kontrollera_server` i `kontroller.py`. Både menyn och kommandoraden anropar den, och `kontrollera_alla` anropar den i en loop. Om jag vill ändra hur kontrollen fungerar behöver jag bara ändra på ett ställe, och det finns ingen risk att två kopior börjar bete sig olika.

**Kommandot till subprocess skickas som en lista.** I `svarar_pa_ping` skrivs kommandot som `["ping", "-c", "1", adress]` och inte som en enda sträng med `shell=True`. Då går adressen in som ett eget argument och kan inte tolkas som ett extra kommando. Om någon skulle skriva t.ex. `localhost; rm -rf ~` som adress händer inget farligt. Jag har också `timeout=5` så att programmet inte hänger om en server inte svarar.

**Konfiguration utanför koden.** Filnamnet läses från miljövariabeln i `hamta_datafil` i stället för att vara hårdkodat överallt. Då kan man byta datafil utan att ändra koden, till exempel använda en testfil. Det finns heller inga lösenord eller hemligheter i koden. Jag har även `.gitignore` så att `__pycache__/` och `rapporter/` inte hamnar i git.

Utöver det har funktionerna och variablerna beskrivande namn i `snake_case` utan å, ä och ö, och varje funktion tar emot det den behöver som parametrar.

## 7. Källor och hjälpmedel

- **Kursmaterialet och Service Status Tool** som vi byggde under kursen. Jag använde det som stöd för hur man delar upp ett program i moduler och hur `argparse`, `subprocess` och JSON fungerar.
- **Pythons officiella dokumentation** (docs.python.org), framför allt sidorna om `argparse`, `csv.DictWriter`, `subprocess.run` och `datetime.strftime`.
- **`man ping`** i terminalen för att se vad flaggan `-c` gör.
- **AI-verktyg** för att få förklaringar när jag fastnade och för att felsöka.
