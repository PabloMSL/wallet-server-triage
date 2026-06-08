import json
import os
import threading

DATA_FILE = "data/accounts.json"
# Mecanismo Mutex para evitar colisiones de hilos en transferencias simultáneas
db_lock = threading.Lock()

def init_db():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "ACC-001": {"titular": "Carlos Mendoza", "saldo": 500000.0, "estado": "ACTIVA", "historial": []},
                "ACC-002": {"titular": "Ana Gomez", "saldo": 12000.0, "estado": "ACTIVA", "historial": []},
                "ACC-003": {"titular": "Juan Perez", "saldo": 1000000.0, "estado": "BLOQUEADA", "historial": []}
            }, f, indent=4)

def load_accounts():
    with db_lock: # El hilo adquiere el candado antes de leer
        with open(DATA_FILE, "r") as f:
            return json.load(f)

def save_accounts(data):
    with db_lock: # El hilo adquiere el candado antes de guardar
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
