MIN_MONTO = 1000
MAX_MONTO = 50000
BONUS_10_THRESHOLD = 10000
BONUS_25_THRESHOLD = 30000
BONUS_10_RATE = 0.10
BONUS_25_RATE = 0.25
PREMIUM_BONUS_RATE = 0.05


def _validar_monto(monto: int) -> str | None:
    if monto < MIN_MONTO or monto > MAX_MONTO:
        return f"El monto debe estar entre ${MIN_MONTO:,} y ${MAX_MONTO:,}"
    return None


def _calcular_tasa_bonificacion(monto: int, plan_premium: bool) -> float:
    if monto >= BONUS_25_THRESHOLD:
        tasa = BONUS_25_RATE
    elif monto >= BONUS_10_THRESHOLD:
        tasa = BONUS_10_RATE
    else:
        tasa = 0.0

    if plan_premium and tasa > 0:
        tasa += PREMIUM_BONUS_RATE

    return tasa


def calcular_recarga(monto: int, plan_premium: bool = False) -> dict:
    error = _validar_monto(monto)
    if error:
        return {"estado": "rechazado", "mensaje": error}

    bonificacion = _calcular_tasa_bonificacion(monto, plan_premium)
    datos_bonificacion = int(monto * bonificacion)
    return {
        "estado": "aprobado",
        "monto_original": monto,
        "bonificacion": bonificacion,
        "datos_bonificacion": datos_bonificacion,
        "monto_final": monto + datos_bonificacion,
    }
