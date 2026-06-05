from app.calculadora import calcular_recarga


class TestValidacionRango:
    def test_rechaza_monto_menor_al_minimo(self):
        resultado = calcular_recarga(500)
        assert resultado["estado"] == "rechazado"

    def test_rechaza_monto_mayor_al_maximo(self):
        resultado = calcular_recarga(60000)
        assert resultado["estado"] == "rechazado"


class TestBonificacion10:
    def test_monto_10k_recibe_10_porciento(self):
        resultado = calcular_recarga(10000)
        assert resultado["bonificacion"] == 0.1

    def test_monto_9999_no_recibe_bonificacion(self):
        resultado = calcular_recarga(9999)
        assert resultado["bonificacion"] == 0.0
