def calcular_recarga(monto: int, plan_premium: bool = False) -> dict:
    if monto < 1000 or monto > 50000:
        return {"estado": "rechazado", "mensaje": "El monto debe estar entre $1.000 y $50.000"}
    return {"estado": "aprobado"}
