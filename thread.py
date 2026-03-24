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