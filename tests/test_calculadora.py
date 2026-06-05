import pytest
from app.calculadora import (
    calcular_recarga,
    _validar_monto,
    _calcular_tasa_bonificacion,
    MIN_MONTO,
    MAX_MONTO,
)


class TestValidacionRango:
    def test_rechaza_monto_menor_al_minimo(self):
        resultado = calcular_recarga(500)
        assert resultado["estado"] == "rechazado"

    def test_rechaza_monto_mayor_al_maximo(self):
        resultado = calcular_recarga(60000)
        assert resultado["estado"] == "rechazado"


class TestValidacionRangoDirecta:
    def test_validar_monto_devuelve_error_si_menor(self):
        assert _validar_monto(MIN_MONTO - 1) is not None

    def test_validar_monto_devuelve_error_si_mayor(self):
        assert _validar_monto(MAX_MONTO + 1) is not None

    def test_validar_monto_devuelve_none_si_valido(self):
        assert _validar_monto(MIN_MONTO) is None
        assert _validar_monto(MAX_MONTO) is None
        assert _validar_monto(25000) is None


class TestBonificacion10:
    def test_monto_10k_recibe_10_porciento(self):
        resultado = calcular_recarga(10000)
        assert resultado["bonificacion"] == 0.1

    def test_monto_9999_no_recibe_bonificacion(self):
        resultado = calcular_recarga(9999)
        assert resultado["bonificacion"] == 0.0


class TestBonificacion25:
    def test_monto_30k_recibe_25_porciento(self):
        resultado = calcular_recarga(30000)
        assert resultado["bonificacion"] == 0.25

    def test_monto_29999_recibe_10_porciento(self):
        resultado = calcular_recarga(29999)
        assert resultado["bonificacion"] == 0.1


class TestCalculoTasaDirecto:
    def test_tasa_0_si_menor_10k(self):
        assert _calcular_tasa_bonificacion(5000, False) == 0.0

    def test_tasa_10_si_entre_10k_y_29999(self):
        assert _calcular_tasa_bonificacion(15000, False) == 0.1

    def test_tasa_25_si_mayor_igual_30k(self):
        assert _calcular_tasa_bonificacion(40000, False) == 0.25

    def test_tasa_15_con_premium_y_10k(self):
        assert _calcular_tasa_bonificacion(10000, True) == pytest.approx(0.15)

    def test_tasa_30_con_premium_y_30k(self):
        assert _calcular_tasa_bonificacion(30000, True) == pytest.approx(0.30)

    def test_tasa_sin_cambio_si_premium_sin_bonificacion(self):
        assert _calcular_tasa_bonificacion(5000, True) == 0.0


class TestPlanPremium:
    def test_premium_con_10k_recibe_15_porciento(self):
        resultado = calcular_recarga(10000, plan_premium=True)
        assert resultado["bonificacion"] == pytest.approx(0.15)

    def test_premium_con_30k_recibe_30_porciento(self):
        resultado = calcular_recarga(30000, plan_premium=True)
        assert resultado["bonificacion"] == pytest.approx(0.30)

    def test_premium_sin_bonificacion_no_recibe_extra(self):
        resultado = calcular_recarga(5000, plan_premium=True)
        assert resultado["bonificacion"] == 0.0


class TestValorFinal:
    def test_monto_final_incluye_datos_bonificacion(self):
        resultado = calcular_recarga(10000)
        esperado = resultado["monto_original"] + resultado["datos_bonificacion"]
        assert resultado["monto_final"] == esperado

    def test_datos_bonificacion_redondea_correctamente(self):
        resultado = calcular_recarga(15000)
        assert resultado["datos_bonificacion"] == 1500  # 10% of 15000

    def test_monto_50000_recibe_25_porciento(self):
        resultado = calcular_recarga(50000)
        assert resultado["bonificacion"] == pytest.approx(0.25)
        assert resultado["datos_bonificacion"] == 12500
        assert resultado["monto_final"] == 62500


class TestValoresLimite:
    def test_monto_999_rechazado(self):
        assert calcular_recarga(999)["estado"] == "rechazado"

    def test_monto_1000_aprobado(self):
        assert calcular_recarga(1000)["estado"] == "aprobado"

    def test_monto_1001_aprobado(self):
        assert calcular_recarga(1001)["estado"] == "aprobado"

    def test_monto_50000_aprobado(self):
        assert calcular_recarga(50000)["estado"] == "aprobado"

    def test_monto_50001_rechazado(self):
        assert calcular_recarga(50001)["estado"] == "rechazado"


class TestMensajeError:
    def test_mensaje_menciona_rango_valido(self):
        resultado = calcular_recarga(500)
        assert "$1,000" in resultado["mensaje"] or "$1.000" in resultado["mensaje"]
