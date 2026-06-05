from pydantic import BaseModel, Field


class RecargaRequest(BaseModel):
    monto: int = Field(..., description="Monto de recarga")
    plan_premium: bool = Field(False, description="Indica si el usuario tiene plan premium")


class RecargaResponse(BaseModel):
    estado: str
    monto_original: int | None = None
    bonificacion: float | None = None
    datos_bonificacion: int | None = None
    monto_final: int | None = None
    mensaje: str | None = None
