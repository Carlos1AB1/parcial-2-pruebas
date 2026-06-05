MIN_MONTO = 1000
MAX_MONTO = 50000


def calcular_recarga(monto: int, plan_premium: bool = False) -> dict:
    if monto < MIN_MONTO or monto > MAX_MONTO:
        return {"estado": "rechazado", "mensaje": f"El monto debe estar entre ${MIN_MONTO:,} y ${MAX_MONTO:,}"}

    if monto >= 10000:
        bonificacion = 0.1
    else:
        bonificacion = 0.0

    datos_bonificacion = int(monto * bonificacion)
    return {
        "estado": "aprobado",
        "monto_original": monto,
        "bonificacion": bonificacion,
        "datos_bonificacion": datos_bonificacion,
        "monto_final": monto + datos_bonificacion,
    }
