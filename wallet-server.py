import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from sistema_bancario.db import init_db
from sistema_bancario.enrutador import run_server

if __name__ == "__main__":
    # Asegura que la base de datos JSON inicial esté creada en la carpeta data/
    init_db()
    # Arranca el servidor seguro en el puerto 8500
    run_server(port=8500)