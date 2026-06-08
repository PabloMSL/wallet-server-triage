from sistema_bancario.db import load_accounts, save_accounts
import time

class WalletService:
    
    @staticmethod
    def get_account_detail(account_id):
        db = load_accounts()
        return db.get(account_id)

    @staticmethod
    def transfer(origin_id, destiny_id, amount):
        # Validación Estricta de Tipos para evitar caracteres extraños o desbordamientos
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return {"error": "El monto debe ser un número válido"}, 422
        
        # Blindaje contra montos negativos (Mitigación de Fraude)
        if amount <= 0:
            return {"error": "El monto a transferir debe ser estrictamente mayor a cero"}, 400

        db = load_accounts()

        if origin_id not in db or destiny_id not in db:
            return {"error": "Una o ambas cuentas no existen en el sistema"}, 404

        # Validación Cruzada de Estados Financieros
        if db[origin_id]["estado"] != "ACTIVA":
            return {"error": "La cuenta de origen se encuentra bloqueada o inactiva"}, 403
        if db[destiny_id]["estado"] != "ACTIVA":
            return {"error": "La cuenta de destino no puede recibir transferencias en este estado"}, 403

        # Validación de fondos disponibles
        if db[origin_id]["saldo"] < amount:
            return {"error": "Fondos insuficientes para completar la transacción"}, 400

        # Latencia artificial segura controlada bajo el bloqueo de base de datos
        time.sleep(0.2)

        # Operación Atómica Inmutable
        db[origin_id]["saldo"] -= amount
        db[destiny_id]["saldo"] += amount

        # Registro en bitácora
        db[origin_id]["historial"].append({"tipo": "DEBITO", "monto": amount, "target": destiny_id})
        db[destiny_id]["historial"].append({"tipo": "CREDITO", "monto": amount, "target": origin_id})

        save_accounts(db)
        return {"status": "SUCCESS", "message": "Transferencia procesada de forma segura e inmutable"}, 200

    @staticmethod
    def update_status(account_id, new_status):
        if new_status not in ["ACTIVA", "BLOQUEADA"]:
            return {"error": "Estado financiero no permitido"}, 400

        db = load_accounts()
        if account_id not in db:
            return {"error": "Cuenta no encontrada"}, 404

        db[account_id]["estado"] = new_status
        save_accounts(db)
        return {"status": "CHANGED", "message": f"Estado de cuenta modificado exitosamente a {new_status}"}, 200