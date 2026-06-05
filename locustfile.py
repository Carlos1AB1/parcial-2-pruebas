import logging
from locust import HttpUser, task, between
from random import randint

logging.getLogger("locust").setLevel(logging.WARNING)


class RecargaUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(3)
    def calcular_recarga_normal(self):
        monto = randint(1000, 50000)
        with self.client.post(
            "/calcular",
            json={"monto": monto, "plan_premium": False},
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")

    @task(1)
    def calcular_recarga_premium(self):
        monto = randint(1000, 50000)
        with self.client.post(
            "/calcular",
            json={"monto": monto, "plan_premium": True},
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")

    @task(1)
    def calcular_recarga_fronteriza(self):
        montos = [999, 1000, 1001, 9999, 10000, 29999, 30000, 49999, 50000, 50001]
        monto = montos[randint(0, len(montos) - 1)]
        with self.client.post(
            "/calcular",
            json={"monto": monto, "plan_premium": False},
            catch_response=True,
        ) as response:
            if response.status_code in (200, 400):
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
