from fastapi import FastAPI, HTTPException
from app.calculadora import calcular_recarga
from app.schemas import RecargaRequest, RecargaResponse

app = FastAPI(
    title="RecargaYa API",
    description="Modulo para calcular el valor final de recargas de celular",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/calcular", response_model=RecargaResponse)
def calcular(request: RecargaRequest):
    resultado = calcular_recarga(request.monto, request.plan_premium)
    if resultado["estado"] == "rechazado":
        raise HTTPException(status_code=400, detail=resultado)
    return resultado
