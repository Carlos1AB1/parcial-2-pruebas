import pytest
from pytest_bdd import scenario, given, when, then, parsers
from app.calculadora import calcular_recarga


@scenario("features/recarga.feature", "Recarga basica exitosa")
def test_recarga_basica_exitosa():
    pass


@scenario("features/recarga.feature", "Recarga rechazada por monto bajo")
def test_recarga_rechazada_bajo():
    pass


@scenario("features/recarga.feature", "Recarga rechazada por monto alto")
def test_recarga_rechazada_alto():
    pass


@scenario("features/recarga.feature", "Recarga con bonificacion del 10%")
def test_recarga_bonificacion_10():
    pass


@scenario("features/recarga.feature", "Recarga con bonificacion del 25%")
def test_recarga_bonificacion_25():
    pass


@scenario("features/recarga.feature", "Recarga premium con bonificacion")
def test_recarga_premium():
    pass


@scenario("features/recarga.feature", "Multiples combinaciones de recarga")
def test_recarga_outline():
    pass


@given(parsers.parse("un monto de recarga de {monto}"), target_fixture="context")
def given_monto(monto):
    return {"monto": int(monto), "plan_premium": False}


@given("el usuario no tiene plan premium")
def given_no_premium(context):
    context["plan_premium"] = False
    return context


@given("el usuario tiene plan premium")
def given_premium(context):
    context["plan_premium"] = True
    return context


@given(parsers.parse("el usuario {tiene_plan} plan premium"))
def given_plan_outline(context, tiene_plan):
    context["plan_premium"] = tiene_plan == "tiene"
    return context


@when("se calcula la recarga", target_fixture="resultado")
def when_calcular(context):
    return calcular_recarga(context["monto"], context["plan_premium"])


@then("la recarga es aprobada")
def then_aprobada(resultado):
    assert resultado["estado"] == "aprobado"


@then("la recarga es rechazada")
def then_rechazada(resultado):
    assert resultado["estado"] == "rechazado"


@then(parsers.parse("la bonificacion es {bonificacion}%"))
def then_bonificacion_porcentaje(resultado, bonificacion):
    assert resultado["bonificacion"] == pytest.approx(float(bonificacion) / 100)


@then(parsers.parse("el monto final es {monto_final}"))
def then_monto_final(resultado, monto_final):
    assert resultado["monto_final"] == int(monto_final)


@then(parsers.parse("el resultado es {estado}"))
def then_estado(resultado, estado):
    assert resultado["estado"] == estado


@then(parsers.parse("la bonificacion es {bonificacion}"))
def then_bonificacion_outline(resultado, bonificacion):
    if bonificacion == "N/A":
        assert resultado["estado"] == "rechazado"
    else:
        assert resultado["bonificacion"] == pytest.approx(float(bonificacion.replace("%", "")) / 100)
