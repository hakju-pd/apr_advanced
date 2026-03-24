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