MIN_MONTO = 1000
MAX_MONTO = 50000


def calcular_recarga(monto: int, plan_premium: bool = False) -> dict:
    if monto < MIN_MONTO or monto > MAX_MONTO:
        return {"estado": "rechazado", "mensaje": f"El monto debe estar entre ${MIN_MONTO:,} y ${MAX_MONTO:,}"}
    return {"estado": "aprobado"}
