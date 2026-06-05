# RecargaYa S.A.S. — Módulo de Cálculo de Recargas

API REST para calcular el valor final de recargas de celular con reglas de bonificación.

## Reglas de negocio

| Regla | Condición | Resultado |
|---|---|---|
| R1 | Monto < $1.000 o > $50.000 | Rechazado |
| R2 | Monto ≥ $10.000 | 10% datos de bonificación |
| R3 | Monto ≥ $30.000 | 25% datos de bonificación (reemplaza R2) |
| R4 | Plan premium | 5% adicional sobre cualquier bonificación |

## Tabla de casos de prueba (partición de equivalencia + valores límite)

| # | Tipo | Monto | Plan | Bonif. esperada |
|---|---|---|---|---|
| 1 | VL inferior inválido | $999 | Normal | Rechazado |
| 2 | VL mínimo válido | $1.000 | Normal | 0% |
| 3 | PE válido bajo | $5.000 | Normal | 0% |
| 4 | VL previo a 10k | $9.999 | Normal | 0% |
| 5 | VL 10k | $10.000 | Normal | 10% |
| 6 | PE medio | $15.000 | Normal | 10% |
| 7 | VL previo a 30k | $29.999 | Normal | 10% |
| 8 | VL 30k | $30.000 | Normal | 25% |
| 9 | PE alto | $40.000 | Normal | 25% |
| 10 | VL máximo válido | $50.000 | Normal | 25% |
| 11 | VL superior inválido | $50.001 | Normal | Rechazado |
| 12 | PE premium 10% | $10.000 | Premium | 15% |
| 13 | PE premium 25% | $30.000 | Premium | 30% |

## Estructura del proyecto

```
.
├── app/
│   ├── calculadora.py      # Lógica de negocio
│   ├── main.py             # API REST con FastAPI
│   └── schemas.py          # Modelos Pydantic
├── tests/
│   ├── test_calculadora.py # Tests unitarios (TDD)
│   ├── test_api.py         # Tests de integración API
│   ├── test_recarga_bdd.py # Steps de BDD
│   └── features/
│       └── recarga.feature # Escenarios Gherkin
├── locustfile.py           # Prueba de carga con Locust
├── requirements.txt
└── .github/workflows/tests.yml
```

## Comandos

### Requisitos

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Tests unitarios

```bash
pytest tests/test_calculadora.py -v
```

### Tests BDD (Gherkin)

```bash
pytest tests/test_recarga_bdd.py -v
```

### Tests de API

```bash
pytest tests/test_api.py -v
```

### Todos los tests

```bash
pytest -v
```

### Servidor local

```bash
uvicorn app.main:app --reload
```

### Prueba de carga con Locust

```bash
# Terminal 1: Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Ejecutar Locust
locust --headless --users 30 --spawn-rate 5 --run-time 30s \
  --host http://localhost:8000 --csv=locust_report
```

## API Endpoints

- `GET /health` — Health check
- `POST /calcular` — Calcular recarga

### Ejemplo de petición

```json
POST /calcular
{
  "monto": 15000,
  "plan_premium": false
}
```

### Respuesta exitosa

```json
{
  "estado": "aprobado",
  "monto_original": 15000,
  "bonificacion": 0.1,
  "datos_bonificacion": 1500,
  "monto_final": 16500
}
```

### Respuesta rechazada (HTTP 400)

```json
{
  "detail": {
    "estado": "rechazado",
    "mensaje": "El monto debe estar entre $1,000 y $50,000"
  }
}
```
