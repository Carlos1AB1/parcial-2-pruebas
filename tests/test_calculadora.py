from app.calculadora import calcular_recarga


class TestValidacionRango:
    def test_rechaza_monto_menor_al_minimo(self):
        resultado = calcular_recarga(500)
        assert resultado["estado"] == "rechazado"

    def test_rechaza_monto_mayor_al_maximo(self):
        resultado = calcular_recarga(60000)
        assert resultado["estado"] == "rechazado"
