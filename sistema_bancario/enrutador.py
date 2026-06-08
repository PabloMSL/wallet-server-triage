import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from sistema_bancario.logica_servicio import WalletService
from sistema_bancario.middleware import SecurityMiddleware

class SecureWalletAPI(BaseHTTPRequestHandler):

    def _response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        url_parsed = urlparse(self.path)
        path = url_parsed.path
        query = parse_qs(url_parsed.query)

        if path == "/api/v1/accounts/detail":
            account_id_list = query.get("id")
            if not account_id_list:
                return self._response({"error": "Falta parámetro 'id'"}, 400)
            account = WalletService.get_account_detail(account_id_list[0])
            if account:
                return self._response(account)
            return self._response({"error": "Cuenta no encontrada"}, 404)
        self._response({"msg": "SecureWallet API Gateway Ready"}, 200)

    def do_POST(self):
        url_parsed = urlparse(self.path)
        path = url_parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body.decode("utf-8")) if content_length > 0 else {}
        except Exception:
            return self._response({"error": "Estructura JSON malformada"}, 400)

        # Enrutamiento seguro hacia la capa de negocio
        if path == "/api/v1/transactions/transfer":
            origin = payload.get("desde")
            destiny = payload.get("hacia")
            amount = payload.get("monto")
            res, status = WalletService.transfer(origin, destiny, amount)
            return self._response(res, status)

        # Endpoint protegido por el Middleware de seguridad
        elif path == "/api/v1/accounts/admin/bypass-status":
            if not SecurityMiddleware.is_authorized(self.headers):
                return self._response({"error: "Acceso Denegado: Requiere Token de Administrador"}, 401)

            acc_id = payload.get("id")
            new_status = payload.get("status")
            res, status = WalletService.update_status(acc_id, new_status)
            return self._response(res, status)

        self._response({"error": "Endpoint inválido"}, 404)

def run_server(port=8500):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SecureWalletAPI)
    print(f"💰 [PRODUCCIÓN] Core Bancario corriendo de forma segura en puerto {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
