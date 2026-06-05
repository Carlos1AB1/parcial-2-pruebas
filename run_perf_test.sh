#!/usr/bin/env bash
set -euo pipefail

echo "=== Iniciando servidor FastAPI ==="
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

cleanup() {
  echo "=== Deteniendo servidor ==="
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "=== Ejecutando Locust (30 usuarios, 30s) ==="
locust --headless \
       --users 30 \
       --spawn-rate 5 \
       --run-time 30s \
       --host http://localhost:8000 \
       --csv=locust_report \
       --only-summary 2>&1 | tee locust_output.txt

echo "=== Verificando P95 < 300ms ==="
python3 -c "
import csv, sys

with open('locust_report_stats.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Name', '').strip()
        if name == '/calcular' or name == 'Aggregated' or 'calcular' in name:
            p95_str = row.get('95%', '').strip()
            if p95_str:
                p95 = float(p95_str)
                print(f'P95 para {name}: {p95}ms')
                if p95 > 300:
                    print(f'ERROR: P95 {p95}ms excede el limite de 300ms')
                    sys.exit(1)
                else:
                    print(f'OK: P95 {p95}ms es menor a 300ms')
                    sys.exit(0)

# Si no encontramos /calcular, buscar en el archivo CSV
with open('locust_report_stats.csv') as f:
    content = f.read()
    print('Contenido del CSV:')
    print(content)
    sys.exit(1)
"
