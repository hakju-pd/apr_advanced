# APR Advanced – 2CK

**Klasse:** 2CK | **Semester:** 2 
**Thema:** Einführung in Threading und Multiprocessing mit Python

---

> 📖 **So arbeitest du mit diesen Unterlagen:**
>
> Diese Unterlagen sind für das **Selbststudium** konzipiert. Du arbeitest eigenständig durch alle Blöcke.
> Jeder Block besteht aus:
> 1. **Theorie** – lesen und verstehen
> 2. **Beispiel** – Code kopieren, ausführen, Ausgabe beobachten
> 3. **Ausprobieren** – Code verändern, Experimente machen
> 4. **Eigene Aufgabe** – selbst implementieren
>
> Bei Fragen: wende dich an den Lehrer. Aber versuche immer zuerst selbst zu googeln oder die Python-Doku zu lesen.

---

## 🗺️ Übersicht

| Block | Thema |
|-------|-------|
| A | Concurrency vs. Parallelism – die Grundbegriffe 
| B | Threads in Python – `threading`-Modul
| C | Thread-Safety & Locks
| D | Der GIL – Pythons große Einschränkung
| E | Multiprocessing – echter Parallelismus
| F | Queues – Kommunikation zwischen Threads/Prozessen
| G | Abschlussprojekt – wähle eine Aufgabe

---

---

## Block A: Concurrency vs. Parallelism – Was ist der Unterschied?

### 📖 Theorie

Bevor wir Code schreiben, müssen wir zwei Begriffe klären die oft verwechselt werden:

#### Concurrency (Nebenläufigkeit)

**Concurrency** bedeutet: Mehrere Aufgaben werden *scheinbar* gleichzeitig erledigt – in Wirklichkeit wechselt die CPU aber sehr schnell zwischen ihnen hin und her.

**Analogie:** Stell dir vor, ein Koch bereitet alleine ein 3-Gänge-Menü zu. Er kocht die Suppe, wartet bis sie köchelt, hackt währenddessen Gemüse für die Hauptspeise, schaut kurz zur Suppe, rührt um, legt den Tisch, schaut wieder zur Suppe... Der Koch macht immer nur *eine* Sache, aber er wechselt schnell zwischen den Aufgaben – es sieht aus als würde er alles gleichzeitig machen.

```
Zeit:  ─────────────────────────────────────────────────────►
CPU:   [Task A][Task B][Task A][Task A][Task B][Task B][Task A]
       ← CPU wechselt schnell zwischen Tasks (Context Switch) →
```

**Gut für:** Aufgaben die viel *warten* (IO-bound) – z.B. auf Netzwerkanfragen, Dateioperationen, Datenbank-Abfragen.

#### Parallelism (Parallelismus)

**Parallelismus** bedeutet: Mehrere Aufgaben werden *wirklich* gleichzeitig auf verschiedenen CPU-Kernen ausgeführt.

**Analogie:** Jetzt hat das Restaurant drei Köche. Einer kocht die Suppe, einer macht die Hauptspeise, einer das Dessert – alle gleichzeitig auf verschiedenen Herdplatten.

```
Zeit:  ─────────────────────────────────────────────────────►
CPU1:  [Task A][Task A][Task A][Task A][Task A][Task A][Task A]
CPU2:  [Task B][Task B][Task B][Task B][Task B][Task B][Task B]
CPU3:  [Task C][Task C][Task C][Task C][Task C][Task C][Task C]
       ← Echte Gleichzeitigkeit auf mehreren CPU-Kernen ►
```

**Gut für:** Aufgaben die viel *rechnen* (CPU-bound) – z.B. Bildverarbeitung, Verschlüsselung, wissenschaftliche Berechnungen.

#### Die zwei Arten von Aufgaben

| Begriff | Bedeutung | Beispiele |
|---------|-----------|---------|
| **IO-bound** | Aufgabe wartet auf Input/Output | Datei lesen, HTTP-Request, Datenbank-Query, Benutzereingabe |
| **CPU-bound** | Aufgabe rechnet intensiv | Mathematische Berechnungen, Bildverarbeitung, Komprimierung |

**Merksatz:**
- IO-bound → **Concurrency** (Threads) ist ideal, weil man die Wartezeit nutzt
- CPU-bound → **Parallelismus** (Multiprocessing) ist nötig, weil man mehrere Kerne braucht

---

### 💻 Beispiel A1: IO-bound vs CPU-bound selbst messen

Führe diesen Code aus und beobachte die Laufzeiten:

```python
# beispiel_a1_bound_types.py
# Demonstriert den Unterschied zwischen IO-bound und CPU-bound Aufgaben

import time

# ─────────────────────────────────────────────────────────────
# IO-BOUND Aufgabe: Warten simulieren (z.B. Netzwerk-Anfrage)
# In der Realität würde hier ein requests.get() stehen
# ─────────────────────────────────────────────────────────────
def io_aufgabe(name):
    """Simuliert eine Aufgabe die viel wartet (z.B. API-Call)."""
    print(f"[{name}] Starte IO-Aufgabe (warte 2 Sekunden)...")
    time.sleep(2)  # Simuliert Wartezeit (Netzwerk, Datei, DB)
    print(f"[{name}] IO-Aufgabe fertig!")


# ─────────────────────────────────────────────────────────────
# CPU-BOUND Aufgabe: Intensives Rechnen
# ─────────────────────────────────────────────────────────────
def cpu_aufgabe(name, n=10_000_000):
    """Simuliert eine CPU-intensive Aufgabe."""
    print(f"[{name}] Starte CPU-Aufgabe ({n:,} Berechnungen)...")
    ergebnis = 0
    for i in range(n):
        ergebnis += i * i  # Sinnlos aber rechenintensiv
    print(f"[{name}] CPU-Aufgabe fertig! Ergebnis: {ergebnis}")
    return ergebnis


# ─────────────────────────────────────────────────────────────
# SEQUENZIELL: Aufgaben nacheinander ausführen
# ─────────────────────────────────────────────────────────────
print("=" * 50)
print("Test: 3x IO-Aufgaben SEQUENZIELL")
print("=" * 50)
start = time.time()

io_aufgabe("Task-1")
io_aufgabe("Task-2")
io_aufgabe("Task-3")

dauer = time.time() - start
print(f"\n⏱ Dauer sequenziell: {dauer:.2f} Sekunden")
print(f"  Erwartung: ~6 Sekunden (3 × 2 Sek)")
```

**Was du siehst:** 3 Aufgaben à 2 Sekunden = ~6 Sekunden. Nacheinander. Langweilig und langsam.

---

### 🔬 Ausprobieren A

Ändere `n=10_000_000` auf `n=1_000_000` und `n=100_000_000`. Was ändert sich an der Laufzeit? Wann merkst du dass dein Computer warm wird?

---

---

## Block B: Threads in Python – `threading`-Modul

### 📖 Theorie

Ein **Thread** ist ein leichtgewichtiger Ausführungspfad innerhalb eines Prozesses. Mehrere Threads teilen sich den **selben Speicher** – das macht sie schnell in der Kommunikation, aber auch anfällig für Fehler (dazu gleich mehr).

**Prozess vs. Thread:**

```
PROZESS (schwer, eigener Speicher)
┌─────────────────────────────────────┐
│ Python-Interpreter                  │
│ Eigener Speicherbereich             │
│                                     │
│  THREAD 1   THREAD 2   THREAD 3    │
│  ────────   ────────   ────────    │
│  Eigener    Eigener    Eigener     │
│  Stack      Stack      Stack       │
│                                     │
│  ← gemeinsamer Heap-Speicher →     │
└─────────────────────────────────────┘
```

Threads innerhalb eines Prozesses teilen sich:
- Globale Variablen
- Geöffnete Dateien
- Netzwerkverbindungen

Jeder Thread hat seinen eigenen:
- Stack (lokale Variablen, Funktionsaufrufe)
- Program Counter (wo bin ich gerade in der Ausführung?)

#### Das `threading`-Modul

```python
import threading

# Thread erstellen:
t = threading.Thread(
    target=meine_funktion,   # Welche Funktion soll der Thread ausführen?
    args=(arg1, arg2),       # Argumente als Tuple
    kwargs={"key": "value"} # Keyword-Argumente als Dict
)

t.start()   # Thread starten (läuft jetzt)
t.join()    # Warten bis der Thread fertig ist
```

**Wichtige Thread-Methoden:**

| Methode/Attribut | Bedeutung |
|-----------------|-----------|
| `t.start()` | Thread starten |
| `t.join()` | Warten bis Thread fertig |
| `t.join(timeout=5)` | Maximal 5 Sekunden warten |
| `t.is_alive()` | Läuft der Thread noch? |
| `t.daemon = True` | Thread stirbt wenn Hauptprogramm endet |
| `t.name` | Name des Threads (für Debugging) |
| `threading.current_thread().name` | Name des aktuellen Threads |
| `threading.active_count()` | Wie viele Threads laufen gerade? |

---

### 💻 Beispiel B1: Erster Thread

```python
# beispiel_b1_erster_thread.py
import threading
import time

def begruessen(name, verzoegerung):
    """Eine einfache Funktion die verzögert ausgeführt wird."""
    time.sleep(verzoegerung)
    print(f"Hallo, {name}! (Thread: {threading.current_thread().name})")

# ─── Ohne Threading ───────────────────────────────────────────
print("=== Ohne Threading ===")
start = time.time()

begruessen("Anna", 1)
begruessen("Ben", 2)
begruessen("Clara", 1.5)

print(f"Dauer: {time.time() - start:.2f} Sek")
# Erwartung: ~4.5 Sekunden

print()

# ─── Mit Threading ────────────────────────────────────────────
print("=== Mit Threading ===")
start = time.time()

# Drei Threads erstellen
t1 = threading.Thread(target=begruessen, args=("Anna",  1),   name="Thread-Anna")
t2 = threading.Thread(target=begruessen, args=("Ben",   2),   name="Thread-Ben")
t3 = threading.Thread(target=begruessen, args=("Clara", 1.5), name="Thread-Clara")

# Alle drei starten (gleichzeitig!)
t1.start()
t2.start()
t3.start()

# Warten bis alle fertig sind
t1.join()
t2.join()
t3.join()

print(f"Dauer: {time.time() - start:.2f} Sek")
# Erwartung: ~2 Sekunden (so lange wie die längste Aufgabe)
```

**Was du siehst:** Mit Threads dauert es nur ~2 Sekunden statt ~4.5 Sekunden – weil alle drei gleichzeitig "warten".

---

### 💻 Beispiel B2: Mehrere Threads mit einer Liste

```python
# beispiel_b2_thread_liste.py
# Eleganter: Threads in einer Liste verwalten

import threading
import time
import random

def download_simulieren(url, ergebnisse, index):
    """
    Simuliert einen HTTP-Download.
    Speichert das Ergebnis im ergebnisse-Dictionary.
    
    Args:
        url:        URL die "heruntergeladen" wird
        ergebnisse: Gemeinsames Dictionary für Ergebnisse
        index:      Schlüssel im Dictionary
    """
    # Zufällige Wartezeit (0.5 bis 3 Sekunden) = simulierter Download
    wartezeit = random.uniform(0.5, 3.0)
    time.sleep(wartezeit)
    
    # Ergebnis speichern (hier: Größe in KB als Zufallszahl)
    groesse_kb = random.randint(50, 5000)
    ergebnisse[index] = {
        "url":      url,
        "groesse":  groesse_kb,
        "dauer":    round(wartezeit, 2)
    }
    print(f"✓ Download fertig: {url} ({groesse_kb} KB in {wartezeit:.2f}s)")


# ─── URLs die "heruntergeladen" werden ─────────────────────────
urls = [
    "https://example.com/datei1.jpg",
    "https://example.com/datei2.pdf",
    "https://example.com/video.mp4",
    "https://api.example.com/daten.json",
    "https://cdn.example.com/bild.png",
]

ergebnisse = {}
threads    = []

print(f"Starte Download von {len(urls)} Dateien...")
start = time.time()

# ─── Für jede URL einen Thread erstellen und starten ──────────
for i, url in enumerate(urls):
    t = threading.Thread(
        target=download_simulieren,
        args=(url, ergebnisse, i),
        name=f"Download-{i+1}"
    )
    threads.append(t)
    t.start()

# ─── Auf alle Threads warten ───────────────────────────────────
for t in threads:
    t.join()

# ─── Auswertung ───────────────────────────────────────────────
gesamt_dauer = time.time() - start
gesamt_kb    = sum(r["groesse"] for r in ergebnisse.values())

print(f"\n{'='*50}")
print(f"Alle Downloads abgeschlossen!")
print(f"Gesamtgröße: {gesamt_kb:,} KB")
print(f"Dauer (parallel): {gesamt_dauer:.2f} Sek")
print(f"Aktive Threads: {threading.active_count()} (nur Hauptthread)")
```

---

### 🔬 Ausprobieren B

1. Ändere `urls` so dass es 20 URLs gibt. Was passiert mit der Gesamtdauer?
2. Was passiert wenn du alle `t.join()`-Aufrufe entfernst? Wann endet das Programm?
3. Füge `print(threading.active_count())` **vor und nach** den `.start()`-Aufrufen ein. Was siehst du?

---

### 📝 Eigene Aufgabe B

Schreibe ein Programm das **5 Temperatur-Messstationen** simuliert:
- Jede Station misst alle 0.5–2 Sekunden (zufällig) eine Temperatur zwischen -10 und +40 Grad
- Jede Station führt genau 3 Messungen durch
- Alle Stationen laufen gleichzeitig (Threads!)
- Am Ende: gib den Durchschnitt aller Messungen aller Stationen aus

```python
# deine_loesung_b.py
import threading
import time
import random

def messstation(station_id, messungen_liste):
    # TODO: Implementiere 3 Messungen mit zufälliger Wartezeit
    # Speichere jede Messung in messungen_liste
    # Gib nach jeder Messung aus: "Station X: YY.Y°C"
    pass

messungen = []
# TODO: Erstelle 5 Threads (eine pro Station), starte sie, warte auf sie
# TODO: Berechne und gib den Gesamtdurchschnitt aus
```

---

---

## Block C: Thread-Safety & Locks

### 📖 Theorie

Da Threads **denselben Speicher teilen**, kann es zu einem gefährlichen Problem kommen: **Race Conditions** (Wettlaufsituationen).

**Was ist eine Race Condition?**

Stell dir vor, zwei Threads lesen gleichzeitig den Wert einer Variable, erhöhen ihn, und schreiben ihn zurück:

```
Thread 1: liest konto = 1000
Thread 2: liest konto = 1000   ← beide lesen denselben Wert!
Thread 1: berechnet 1000 + 100 = 1100
Thread 2: berechnet 1000 - 200 = 800
Thread 1: schreibt konto = 1100
Thread 2: schreibt konto = 800  ← Thread 1's Änderung ist weg!

Erwartet: 1000 + 100 - 200 = 900
Tatsächlich: 800 (Thread 1's Einzahlung ist verschwunden!)
```

Das ist wie wenn zwei Menschen gleichzeitig eine Tür öffnen wollen – ohne Absprache gibt es ein Chaos.

**Lösung: Lock (Mutex)**

Ein `Lock` (auch Mutex = Mutual Exclusion) stellt sicher, dass immer nur **ein Thread** auf eine Ressource zugreift:

```python
import threading

lock = threading.Lock()

# Thread sicherer Zugriff:
with lock:          # Lock wird acquired (gesperrt)
    # Kritischer Abschnitt – nur ein Thread kann hier gleichzeitig sein
    konto += 100
# Lock wird automatisch released (entsperrt) beim Verlassen des with-Blocks
```

**Wie ein Lock funktioniert:**
- `lock.acquire()` → Thread wartet falls Lock schon belegt ist
- `lock.release()` → Lock freigeben (andere Threads können jetzt rein)
- `with lock:` → acquire + release automatisch (empfohlen!)

---

### 💻 Beispiel C1: Race Condition demonstrieren (kaputt!)

```python
# beispiel_c1_race_condition.py
# ABSICHTLICH KAPUTT – zeigt was ohne Lock passiert

import threading
import time

# Gemeinsame Variable (wird von mehreren Threads verändert)
konto_stand = 0
ANZAHL_THREADS = 1000
BETRAG_PRO_THREAD = 1

def einzahlen():
    """Zahlt BETRAG_PRO_THREAD auf das Konto ein."""
    global konto_stand
    
    # ⚠️ OHNE LOCK – RACE CONDITION MÖGLICH!
    # Diese drei Operationen sind NICHT atomar:
    aktuell = konto_stand      # 1. Lesen
    time.sleep(0.00001)        # Simuliert dass zwischen Lesen und Schreiben Zeit vergeht
    konto_stand = aktuell + BETRAG_PRO_THREAD  # 2. Berechnen + 3. Schreiben

# Erstelle ANZAHL_THREADS Threads
threads = []
for i in range(ANZAHL_THREADS):
    t = threading.Thread(target=einzahlen)
    threads.append(t)

# Alle starten
for t in threads:
    t.start()

# Alle warten
for t in threads:
    t.join()

erwartet  = ANZAHL_THREADS * BETRAG_PRO_THREAD
tatsaechl = konto_stand

print(f"Erwartet:    {erwartet}")
print(f"Tatsächlich: {tatsaechl}")
print(f"Verloren:    {erwartet - tatsaechl}")
print(f"Korrekt: {'✅' if erwartet == tatsaechl else '❌ RACE CONDITION!'}")
```

---

### 💻 Beispiel C2: Lock – die Lösung

```python
# beispiel_c2_mit_lock.py
# Dieselbe Situation, diesmal THREAD-SICHER mit Lock

import threading
import time

konto_stand = 0
lock        = threading.Lock()   # Ein Lock für das Konto

ANZAHL_THREADS = 1000
BETRAG_PRO_THREAD = 1

def einzahlen_sicher():
    """Thread-sichere Einzahlung mit Lock."""
    global konto_stand
    
    # with lock: stellt sicher dass nur EIN Thread diesen Block betritt
    with lock:
        aktuell = konto_stand
        time.sleep(0.00001)
        konto_stand = aktuell + BETRAG_PRO_THREAD

threads = []
for i in range(ANZAHL_THREADS):
    t = threading.Thread(target=einzahlen_sicher)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

erwartet  = ANZAHL_THREADS * BETRAG_PRO_THREAD
tatsaechl = konto_stand

print(f"Erwartet:    {erwartet}")
print(f"Tatsächlich: {tatsaechl}")
print(f"Korrekt: {'✅ THREAD-SICHER!' if erwartet == tatsaechl else '❌ FEHLER'}")
```

---

### 💻 Beispiel C3: Mehrere Locks – Deadlock-Gefahr

```python
# beispiel_c3_deadlock_demo.py
# Zeigt wie ein Deadlock entsteht (Programm hängt für immer)
# VORSICHT: Dieses Programm hängt! Mit Ctrl+C abbrechen.

import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1_funktion():
    """Thread 1: holt zuerst Lock A, dann Lock B."""
    print("Thread 1: Warte auf Lock A...")
    with lock_a:
        print("Thread 1: Hat Lock A! Warte 0.1 Sek...")
        time.sleep(0.1)   # Gibt Thread 2 Zeit Lock B zu holen
        
        print("Thread 1: Versuche Lock B zu bekommen...")
        with lock_b:
            print("Thread 1: Hat beide Locks!")

def thread_2_funktion():
    """Thread 2: holt zuerst Lock B, dann Lock A – umgekehrte Reihenfolge!"""
    print("Thread 2: Warte auf Lock B...")
    with lock_b:
        print("Thread 2: Hat Lock B! Warte 0.1 Sek...")
        time.sleep(0.1)
        
        print("Thread 2: Versuche Lock A zu bekommen...")
        with lock_a:   # ← DEADLOCK! Thread 1 hat Lock A und wartet auf B
            print("Thread 2: Hat beide Locks!")

# Was passiert:
# Thread 1 bekommt Lock A
# Thread 2 bekommt Lock B
# Thread 1 wartet auf Lock B (das Thread 2 hält)
# Thread 2 wartet auf Lock A (das Thread 1 hält)
# → Beide warten für immer! = DEADLOCK

print("WARNUNG: Dieses Programm wird hängen bleiben!")
print("Drücke Ctrl+C um es zu beenden.\n")

t1 = threading.Thread(target=thread_1_funktion, name="Thread-1")
t2 = threading.Thread(target=thread_2_funktion, name="Thread-2")

t1.start()
t2.start()

t1.join(timeout=3)   # Maximal 3 Sekunden warten
t2.join(timeout=3)

if t1.is_alive() or t2.is_alive():
    print("\n💀 DEADLOCK erkannt! Das Programm hängt.")
    print("Lösung: Immer Locks in derselben Reihenfolge acquiren!")
```

---

### 🔬 Ausprobieren C

1. Führe Beispiel C1 mehrmals aus. Ist das Ergebnis immer gleich schlecht? Warum nicht?
2. Ändere in C1 `time.sleep(0.00001)` zu `time.sleep(0)`. Wie verändert sich die Race Condition?
3. Entferne in C3 die `time.sleep(0.1)`-Zeilen. Passiert immer noch ein Deadlock?

---

### 📝 Eigene Aufgabe C

**Bankkonten-Simulation:**

Erstelle eine Simulation mit zwei Bankkonten (Konto A: 1000€, Konto B: 500€).

Implementiere zwei Operationen die gleichzeitig in Threads laufen:
- `ueberweisen(von, nach, betrag)` – überweist einen Betrag
- `kontostand_pruefen(konto)` – liest den Stand

Starte 100 Threads die gleichzeitig überweisen (kleine, zufällige Beträge).

**Anforderungen:**
- Die Gesamtsumme beider Konten muss am Ende immer noch 1500€ sein!
- Verwende Locks damit keine Race Conditions entstehen
- Gib am Ende aus: `Konto A: X€ | Konto B: Y€ | Summe: Z€`

```python
# deine_loesung_c.py
import threading
import random

konto_a = 1000
konto_b = 500
lock    = threading.Lock()

def ueberweisen(von, nach, betrag):
    # TODO: Überweisung thread-sicher implementieren
    # Wenn "von" nicht genug Guthaben hat: abbrechen
    pass

# TODO: 100 Threads starten die zufällige Beträge zwischen 1-50€ überweisen
# TODO: Abwechselnd von A→B und B→A
# TODO: Am Ende: Kontostand ausgeben und prüfen ob Summe = 1500€
```

---

---

## Block D: Der GIL – Pythons große Einschränkung

### 📖 Theorie

Hier kommt der wichtigste Grund warum **Python-Threads keine echte Parallelität für CPU-intensive Aufgaben liefern**:

#### Der Global Interpreter Lock (GIL)

Der GIL ist ein Mutex (Lock) im Python-Interpreter selbst, der sicherstellt, dass **immer nur ein Thread Python-Bytecode ausführt** – auch auf Mehrkern-CPUs!

```
CPU1  CPU2  CPU3  CPU4
 ↓
[Python Interpreter]
      GIL ← Nur ein Thread darf den Interpreter nutzen
[Thread1][Thread2][Thread3]
```

**Warum gibt es den GIL?**

CPython (die Standard-Python-Implementation) verwendet intern Referenz-Counting für Memory Management. Ohne GIL könnten zwei Threads gleichzeitig denselben Referenz-Zähler ändern → Speicherfehler, Crashes.

Guido van Rossum (Python-Erfinder) hat den GIL als pragmatische Lösung eingebaut: besser als komplexe Thread-sichere Datenstrukturen, aber hat Konsequenzen für CPU-bound Tasks.

**Konsequenz des GIL:**

| Aufgabentyp | Mit Threads | Mit Multiprocessing |
|-------------|------------|-------------------|
| IO-bound (Warten) | ✅ Schneller | ✅ Auch schneller |
| CPU-bound (Rechnen) | ❌ Nicht schneller (GIL!) | ✅ Deutlich schneller |

> **Kurz gesagt:** Für IO-bound Tasks → Threads. Für CPU-bound Tasks → Multiprocessing (oder C-Extensions wie NumPy die den GIL freigeben).

---

### 💻 Beispiel D1: GIL in Aktion – CPU-bound mit Threads hilft nicht

```python
# beispiel_d1_gil_beweis.py
# Zeigt dass Threads CPU-bound Tasks NICHT beschleunigen

import threading
import time

def schweres_rechnen(n=50_000_000):
    """CPU-intensive Berechnung."""
    ergebnis = 0
    for i in range(n):
        ergebnis += i * i
    return ergebnis

# ─── Test 1: Sequenziell (1 Thread) ──────────────────────────
print("Test 1: Sequenziell (2 Berechnungen nacheinander)")
start = time.time()
schweres_rechnen()
schweres_rechnen()
dauer_seq = time.time() - start
print(f"Dauer: {dauer_seq:.2f} Sek\n")

# ─── Test 2: Mit 2 Threads ────────────────────────────────────
print("Test 2: Mit 2 Threads (parallel?)")
start = time.time()

t1 = threading.Thread(target=schweres_rechnen)
t2 = threading.Thread(target=schweres_rechnen)

t1.start()
t2.start()
t1.join()
t2.join()

dauer_threads = time.time() - start
print(f"Dauer: {dauer_threads:.2f} Sek\n")

# ─── Vergleich ────────────────────────────────────────────────
print("=" * 40)
print(f"Sequenziell: {dauer_seq:.2f} Sek")
print(f"Mit Threads: {dauer_threads:.2f} Sek")

if dauer_threads >= dauer_seq * 0.9:  # Kein signifikanter Speedup
    print("⚠️  Kein Speedup! Das ist der GIL in Aktion.")
    print("    Threads kämpfen um den GIL → kein echter Parallelismus.")
else:
    print("✅ Speedup vorhanden (selten bei reinen Python CPU-Tasks!)")
```

---

### 🔬 Ausprobieren D

1. Führe Beispiel D1 auf deinem Computer aus. Ist der Thread-Ansatz wirklich gleich schnell oder sogar langsamer?
2. Erhöhe auf `n=100_000_000`. Ändert sich das Verhältnis?
3. **Denk nach:** Warum hilft der GIL immer noch bei IO-bound Tasks obwohl er Threads blockiert?  
   *(Tipp: Was passiert mit dem GIL wenn ein Thread auf `time.sleep()` oder ein Netzwerk-Paket wartet?)*

---

---

## Block E: Multiprocessing – echter Parallelismus

### 📖 Theorie

Da der GIL Threads für CPU-bound Tasks nutzlos macht, gibt es `multiprocessing`: Statt Threads werden **separate Python-Prozesse** gestartet – jeder mit seinem eigenen Interpreter und eigenem GIL.

```
PROZESS 1 (eigener Interpreter)    PROZESS 2 (eigener Interpreter)
┌────────────────────────────┐     ┌────────────────────────────┐
│ Python + GIL               │     │ Python + GIL               │
│ Läuft auf CPU-Kern 1       │     │ Läuft auf CPU-Kern 2       │
│ Eigener Speicher            │     │ Eigener Speicher            │
└────────────────────────────┘     └────────────────────────────┘
← kein gemeinsamer Speicher → Kommunikation via Queue/Pipe
```

**Nachteile von Multiprocessing:**
- Prozesse starten langsamer als Threads (~100ms pro Prozess)
- Kein gemeinsamer Speicher → Daten müssen via Queue/Pipe ausgetauscht werden
- Mehr Speicherverbrauch

**API ist fast identisch zu `threading`:**

```python
from multiprocessing import Process, Pool, Queue

# Einzelner Prozess (wie threading.Thread):
p = Process(target=meine_funktion, args=(arg1, arg2))
p.start()
p.join()

# Pool (mehrere Prozesse verwalten):
with Pool(processes=4) as pool:
    ergebnisse = pool.map(meine_funktion, liste_von_argumenten)
```

---

### 💻 Beispiel E1: Multiprocessing vs. Threading – CPU-bound

```python
# beispiel_e1_multiprocessing_vergleich.py
# Zeigt dass Multiprocessing CPU-bound Tasks wirklich beschleunigt

import threading
import multiprocessing
import time

def schweres_rechnen(n=40_000_000):
    """CPU-intensive Berechnung."""
    ergebnis = 0
    for i in range(n):
        ergebnis += i * i
    return ergebnis

# ─── Sequenziell ──────────────────────────────────────────────
print("1. Sequenziell:")
start = time.time()
schweres_rechnen()
schweres_rechnen()
schweres_rechnen()
schweres_rechnen()
dauer_seq = time.time() - start
print(f"   Dauer: {dauer_seq:.2f} Sek")

# ─── Mit Threads (GIL verhindert echte Parallelität) ──────────
print("\n2. Mit Threads (4 Threads):")
start = time.time()

threads = [threading.Thread(target=schweres_rechnen) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

dauer_threads = time.time() - start
print(f"   Dauer: {dauer_threads:.2f} Sek")

# ─── Mit Multiprocessing (echter Parallelismus) ───────────────
print("\n3. Mit Multiprocessing (4 Prozesse):")
start = time.time()

prozesse = [multiprocessing.Process(target=schweres_rechnen) for _ in range(4)]
for p in prozesse: p.start()
for p in prozesse: p.join()

dauer_mp = time.time() - start
print(f"   Dauer: {dauer_mp:.2f} Sek")

# ─── Auswertung ───────────────────────────────────────────────
print(f"\n{'='*45}")
print(f"Sequenziell:      {dauer_seq:.2f} Sek  (Baseline)")
print(f"Threads (4):      {dauer_threads:.2f} Sek  (Speedup: {dauer_seq/dauer_threads:.1f}x)")
print(f"Prozesse (4):     {dauer_mp:.2f} Sek  (Speedup: {dauer_seq/dauer_mp:.1f}x)")
print(f"\nDein Computer hat {multiprocessing.cpu_count()} CPU-Kerne.")
```

---

### 💻 Beispiel E2: Pool – der einfachste Weg für Parallelismus

```python
# beispiel_e2_pool.py
# Pool.map() – verteilt eine Liste von Aufgaben auf mehrere Prozesse

from multiprocessing import Pool, cpu_count
import time

def ist_primzahl(n):
    """Prüft ob n eine Primzahl ist."""
    if n < 2:
        return (n, False)
    if n == 2:
        return (n, True)
    if n % 2 == 0:
        return (n, False)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return (n, False)
    return (n, True)


if __name__ == "__main__":   # ← WICHTIG bei Multiprocessing auf Windows/macOS!
    # Zahlen die geprüft werden sollen
    zahlen = list(range(1, 100_001))   # 1 bis 100.000
    
    kerne = cpu_count()
    print(f"CPU-Kerne verfügbar: {kerne}")
    
    # ─── Sequenziell ──────────────────────────────────────────
    print("\nSequenziell...")
    start = time.time()
    ergebnisse_seq = [ist_primzahl(n) for n in zahlen]
    dauer_seq = time.time() - start
    
    primzahlen = [n for n, ist_prim in ergebnisse_seq if ist_prim]
    print(f"Primzahlen bis 100.000: {len(primzahlen)}")
    print(f"Dauer sequenziell: {dauer_seq:.2f} Sek")
    
    # ─── Mit Pool ─────────────────────────────────────────────
    print("\nMit Pool...")
    start = time.time()
    
    with Pool(processes=kerne) as pool:
        # pool.map() verteilt zahlen auf alle Prozesse
        # Jeder Prozess ruft ist_primzahl() für seinen Anteil auf
        ergebnisse_mp = pool.map(ist_primzahl, zahlen)
    
    dauer_mp = time.time() - start
    
    primzahlen_mp = [n for n, ist_prim in ergebnisse_mp if ist_prim]
    print(f"Primzahlen bis 100.000: {len(primzahlen_mp)}")
    print(f"Dauer mit Pool:    {dauer_mp:.2f} Sek")
    print(f"Speedup:           {dauer_seq/dauer_mp:.1f}x")
```

> **Wichtig:** `if __name__ == "__main__":` ist bei `multiprocessing` auf Windows/macOS **zwingend erforderlich**! Ohne das spawnen sich Prozesse rekursiv und das Programm crasht.

---

### 🔬 Ausprobieren E

1. Ändere `Pool(processes=kerne)` zu `Pool(processes=1)`, dann `2`, dann `4`. Wie verändert sich der Speedup?
2. Ändere den Zahlenbereich auf `range(1, 1_000_001)`. Wächst der Speedup proportional?
3. Was passiert wenn du `Pool(processes=100)` setzt – mehr als CPU-Kerne vorhanden sind?

---

### 📝 Eigene Aufgabe E

**Bildverarbeitung simulieren:**

Du hast 20 "Bilder" (simuliert als große Listen von Zahlen). Jedes Bild wird "bearbeitet" (jede Zahl quadriert, dann Summe berechnet).

Implementiere:
1. Sequenzielle Verarbeitung
2. Parallele Verarbeitung mit `Pool`
3. Vergleich der Laufzeiten

```python
# deine_loesung_e.py
from multiprocessing import Pool
import time
import random

def bild_verarbeiten(bild_daten):
    """Simuliert Bildverarbeitung: alle Pixel quadrieren."""
    # TODO: Jedes Element der Liste quadrieren und Summe zurückgeben
    pass

if __name__ == "__main__":
    # 20 "Bilder" – jedes hat 500.000 "Pixel" (zufällige Zahlen)
    bilder = [[random.randint(0, 255) for _ in range(500_000)] for _ in range(20)]
    
    # TODO: Sequenziell verarbeiten + Zeit messen
    # TODO: Mit Pool verarbeiten + Zeit messen
    # TODO: Ergebnisse vergleichen (müssen identisch sein!)
    # TODO: Speedup berechnen
```

---

---

## Block F: Queues – Kommunikation zwischen Threads/Prozessen

### 📖 Theorie

Da Prozesse keinen gemeinsamen Speicher haben, brauchen sie einen anderen Weg um Daten auszutauschen. Auch bei Threads ist es oft sauberer, über Queues zu kommunizieren als direkt auf gemeinsame Variablen zuzugreifen.

**Queue** = eine thread-/prozess-sichere FIFO-Warteschlange:

```
Producer Thread/Prozess          Consumer Thread/Prozess
        │                                 │
        ▼                                 ▼
    put("Aufgabe 1") ──► [Queue] ──► get() → "Aufgabe 1"
    put("Aufgabe 2") ──► [Queue] ──► get() → "Aufgabe 2"
    put("Aufgabe 3") ──► [Queue] ──► get() → "Aufgabe 3"
```

**Producer-Consumer-Pattern:** Ein Thread/Prozess produziert Aufgaben, ein anderer konsumiert sie.

| Methode | Bedeutung |
|---------|-----------|
| `q.put(item)` | Element einreihen (blockiert wenn Queue voll) |
| `q.get()` | Element entnehmen (blockiert wenn Queue leer) |
| `q.get(timeout=5)` | Max. 5 Sek warten |
| `q.empty()` | Ist die Queue leer? |
| `q.qsize()` | Wie viele Elemente? |
| `q.put(None)` | Sentinel-Wert – signalisiert "Ende" |

---

### 💻 Beispiel F1: Producer-Consumer mit Threading

```python
# beispiel_f1_queue_threading.py
# Producer-Consumer Pattern: ein Thread erzeugt Aufgaben, mehrere konsumieren sie

import threading
import queue
import time
import random

# Thread-sichere Queue (aus threading-kompatiblem queue-Modul)
aufgaben_queue = queue.Queue(maxsize=10)   # Maximal 10 Aufgaben gleichzeitig

def producer(anzahl_aufgaben):
    """Erzeugt Aufgaben und legt sie in die Queue."""
    for i in range(anzahl_aufgaben):
        aufgabe = f"Aufgabe-{i+1}"
        aufgaben_queue.put(aufgabe)          # Legt Aufgabe ein (blockiert wenn voll)
        print(f"[Producer] Erstellt: {aufgabe} | Queue-Größe: {aufgaben_queue.qsize()}")
        time.sleep(random.uniform(0.1, 0.5))  # Produziert in unregelmäßigen Abständen
    
    # Sentinel-Werte: sagt jedem Consumer "ich bin fertig"
    # Wenn es 3 Consumer gibt, brauchen wir 3 Sentinels
    for _ in range(3):
        aufgaben_queue.put(None)
    
    print("[Producer] Alle Aufgaben erstellt!")

def consumer(consumer_id):
    """Holt Aufgaben aus der Queue und verarbeitet sie."""
    while True:
        aufgabe = aufgaben_queue.get()   # Holt nächste Aufgabe (blockiert wenn leer)
        
        if aufgabe is None:              # Sentinel-Wert = fertig
            print(f"[Consumer-{consumer_id}] Erhalte Stop-Signal, beende.")
            aufgaben_queue.task_done()
            break
        
        # Aufgabe verarbeiten:
        verarbeitungszeit = random.uniform(0.2, 1.0)
        time.sleep(verarbeitungszeit)    # Simuliert Arbeit
        
        print(f"[Consumer-{consumer_id}] Fertig mit {aufgabe} ({verarbeitungszeit:.2f}s)")
        aufgaben_queue.task_done()       # Signalisiert dass Aufgabe erledigt ist

# ─── Start ────────────────────────────────────────────────────
print("Starte Producer-Consumer System...\n")
start = time.time()

# 1 Producer, 3 Consumer
p  = threading.Thread(target=producer, args=(15,), name="Producer")
c1 = threading.Thread(target=consumer, args=(1,),  name="Consumer-1")
c2 = threading.Thread(target=consumer, args=(2,),  name="Consumer-2")
c3 = threading.Thread(target=consumer, args=(3,),  name="Consumer-3")

p.start()
c1.start()
c2.start()
c3.start()

p.join()
c1.join()
c2.join()
c3.join()

print(f"\n⏱ Gesamtdauer: {time.time() - start:.2f} Sek")
```

---

### 💻 Beispiel F2: Queue mit Multiprocessing

```python
# beispiel_f2_queue_multiprocessing.py
# Dieselbe Idee, aber mit echten Prozessen (kein GIL!)

from multiprocessing import Process, Queue
import time
import random

def worker_prozess(prozess_id, aufgaben_queue, ergebnis_queue):
    """
    Nimmt Aufgaben aus aufgaben_queue,
    verarbeitet sie (CPU-intensiv simuliert),
    legt Ergebnis in ergebnis_queue.
    """
    while True:
        aufgabe = aufgaben_queue.get()
        
        if aufgabe is None:   # Sentinel
            break
        
        # CPU-intensive Verarbeitung simulieren
        ergebnis = sum(i * i for i in range(aufgabe * 1000))
        ergebnis_queue.put((prozess_id, aufgabe, ergebnis))

if __name__ == "__main__":
    aufgaben_q  = Queue()
    ergebnisse_q = Queue()
    
    ANZAHL_PROZESSE = 4
    ANZAHL_AUFGABEN = 20
    
    # Aufgaben einreihen (Zahlen 1-20)
    for i in range(1, ANZAHL_AUFGABEN + 1):
        aufgaben_q.put(i)
    
    # Sentinel-Werte
    for _ in range(ANZAHL_PROZESSE):
        aufgaben_q.put(None)
    
    # Prozesse starten
    prozesse = []
    for pid in range(ANZAHL_PROZESSE):
        p = Process(
            target=worker_prozess,
            args=(pid, aufgaben_q, ergebnisse_q)
        )
        prozesse.append(p)
        p.start()
    
    # Warten
    for p in prozesse:
        p.join()
    
    # Ergebnisse auslesen
    print(f"Verarbeitete Aufgaben:")
    while not ergebnisse_q.empty():
        pid, aufgabe, ergebnis = ergebnisse_q.get()
        print(f"  Prozess {pid}: Aufgabe {aufgabe} → {ergebnis}")
```

---

### 🔬 Ausprobieren F

1. Erhöhe `maxsize=10` auf `maxsize=1`. Was ändert sich am Verhalten des Producers?
2. Reduziere die Consumer auf 1. Wie verändert sich die Gesamtdauer?
3. Was passiert wenn du die Sentinel-Werte weglässt? Läuft das Programm jemals zu Ende?

---

### 📝 Eigene Aufgabe F

**Web-Scraping-Simulator:**

Baue ein System das Webseiten "scraped" (simuliert):

- **Producer:** Erzeugt 20 URLs (`"https://example.com/seite-{i}"`) und legt sie in eine Queue
- **Worker-Threads (3 Stück):** Nehmen eine URL, "laden" sie (random 0.5–2 Sek), extrahieren "Titel" und "Wörteranzahl" (zufällig), legen Ergebnis in eine Ergebnis-Queue
- **Hauptprogramm:** Liest Ergebnis-Queue am Ende, gibt die 3 Seiten mit den meisten Wörtern aus

```python
# deine_loesung_f.py
import threading
import queue
import time
import random

aufgaben_q  = queue.Queue()
ergebnis_q  = queue.Queue()

def url_scrapen(worker_id):
    # TODO: URLs aus aufgaben_q holen, verarbeiten, in ergebnis_q legen
    pass

def producer():
    # TODO: 20 URLs in aufgaben_q legen, dann Sentinels
    pass

# TODO: Producer + 3 Worker-Threads starten und warten
# TODO: Top-3 Seiten nach Wörteranzahl ausgeben
```

---

---

## Block G: Abschlussprojekt – Wähle eine Aufgabe

Bearbeite **eine** der folgenden Aufgaben. Alle sind in ~15 Minuten lösbar wenn du die Blöcke A–F verstanden hast.

---

### 🥇 Option 1: Ping-Scanner (Threading, IO-bound)

Schreibe einen einfachen Netzwerk-Scanner der mehrere IPs gleichzeitig "pingt":

```python
# Statt echtem Ping: simuliere ob eine "IP" erreichbar ist
# IP ist erreichbar wenn: int(ip.split(".")[-1]) % 3 != 0  (zufällige Regel)

# Scanne 192.168.1.1 bis 192.168.1.50 gleichzeitig mit 10 Threads
# Ausgabe: welche IPs sind erreichbar?
# Miss die Zeit: sequenziell vs. parallel
```

---

### 🥈 Option 2: Parallele Dateiverarbeitung (Multiprocessing, CPU-bound)

```python
# Generiere 10 "Textdateien" (Listen von 100.000 zufälligen Wörtern)
# Jede Datei soll "analysiert" werden:
#   - Häufigstes Wort finden
#   - Durchschnittliche Wortlänge berechnen
#   - Anzahl eindeutiger Wörter
# 
# Implementiere: sequenziell und mit Pool
# Vergleiche Laufzeiten
```

---

### 🥉 Option 3: Thread-sicherer Log-Aggregator

```python
# 10 Threads erzeugen gleichzeitig Log-Einträge
# Format: "[Thread-X | HH:MM:SS.mmm] Nachricht"
# Alle Logs werden in einer gemeinsamen Liste gespeichert
# 
# Anforderungen:
# - Reihenfolge der Logs muss korrekt sein (Lock verwenden!)
# - Am Ende: Logs nach Zeit sortiert ausgeben
# - Zeige: wie viele Logs hat jeder Thread erzeugt?
```

---

## ✅ Abschluss-Checkliste

Bevor du fertig bist, beantworte diese Fragen schriftlich (direkt im Code als Kommentare):

```python
# REFLEXION:
# 1. Wann sollte man Threads verwenden, wann Multiprocessing?
# 2. Was ist der GIL und warum ist er für CPU-bound Tasks ein Problem?
# 3. Was ist eine Race Condition? Wie verhindert man sie?
# 4. Wann braucht man einen Lock? Wann reicht eine Queue?
# 5. Was ist das Producer-Consumer-Pattern und wann ist es sinnvoll?
```

---

## 📚 Weiterführende Ressourcen

- **Python Docs – threading:** https://docs.python.org/3/library/threading.html
- **Python Docs – multiprocessing:** https://docs.python.org/3/library/multiprocessing.html
- **Real Python – Python Threading:** https://realpython.com/intro-to-python-threading/
- **Real Python – Python GIL:** https://realpython.com/python-gil/
- **YouTube – Computerphile „Deadlock":** Suche nach "Computerphile Deadlock"
