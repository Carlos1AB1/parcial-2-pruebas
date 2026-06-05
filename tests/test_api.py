import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealth:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestCalcularRecarga:
    def test_recarga_exitosa_sin_bonificacion(self):
        response = client.post("/calcular", json={"monto": 5000, "plan_premium": False})
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "aprobado"
        assert data["bonificacion"] == 0.0
        assert data["monto_final"] == 5000

    def test_recarga_con_bonificacion_10(self):
        response = client.post("/calcular", json={"monto": 10000, "plan_premium": False})
        assert response.status_code == 200
        data = response.json()
        assert data["bonificacion"] == pytest.approx(0.1)
        assert data["monto_final"] == 11000

    def test_recarga_con_bonificacion_25(self):
        response = client.post("/calcular", json={"monto": 30000, "plan_premium": False})
        assert response.status_code == 200
        data = response.json()
        assert data["bonificacion"] == pytest.approx(0.25)
        assert data["monto_final"] == 37500

    def test_recarga_con_premium(self):
        response = client.post("/calcular", json={"monto": 10000, "plan_premium": True})
        assert response.status_code == 200
        data = response.json()
        assert data["bonificacion"] == pytest.approx(0.15)
        assert data["monto_final"] == 11500

    def test_recarga_rechazada_monto_bajo(self):
        response = client.post("/calcular", json={"monto": 500, "plan_premium": False})
        assert response.status_code == 400
        assert response.json()["detail"]["estado"] == "rechazado"

    def test_recarga_rechazada_monto_alto(self):
        response = client.post("/calcular", json={"monto": 60000, "plan_premium": False})
        assert response.status_code == 400
        assert response.json()["detail"]["estado"] == "rechazado"
