Feature: Calculo de Recargas
  Como usuario de RecargaYa S.A.S.
  Quiero calcular el valor final de mi recarga
  Para conocer mi saldo total incluyendo bonificaciones

  Scenario: Recarga basica exitosa
    Given un monto de recarga de 5000
    And el usuario no tiene plan premium
    When se calcula la recarga
    Then la recarga es aprobada
    And la bonificacion es 0%
    And el monto final es 5000

  Scenario: Recarga rechazada por monto bajo
    Given un monto de recarga de 500
    And el usuario no tiene plan premium
    When se calcula la recarga
    Then la recarga es rechazada

  Scenario: Recarga rechazada por monto alto
    Given un monto de recarga de 60000
    And el usuario no tiene plan premium
    When se calcula la recarga
    Then la recarga es rechazada

  Scenario: Recarga con bonificacion del 10%
    Given un monto de recarga de 15000
    And el usuario no tiene plan premium
    When se calcula la recarga
    Then la recarga es aprobada
    And la bonificacion es 10%
    And el monto final es 16500

  Scenario: Recarga con bonificacion del 25%
    Given un monto de recarga de 40000
    And el usuario no tiene plan premium
    When se calcula la recarga
    Then la recarga es aprobada
    And la bonificacion es 25%
    And el monto final es 50000

  Scenario: Recarga premium con bonificacion
    Given un monto de recarga de 10000
    And el usuario tiene plan premium
    When se calcula la recarga
    Then la recarga es aprobada
    And la bonificacion es 15%
    And el monto final es 11500

  Scenario Outline: Multiples combinaciones de recarga
    Given un monto de recarga de <monto>
    And el usuario <plan> plan premium
    When se calcula la recarga
    Then el resultado es <estado>
    And la bonificacion es <bonificacion>

    Examples:
      | monto | plan    | estado     | bonificacion |
      | 1000  | no tiene| aprobado   | 0%           |
      | 999   | no tiene| rechazado  | N/A          |
      | 50000 | no tiene| aprobado   | 25%          |
      | 50001 | no tiene| rechazado  | N/A          |
      | 30000 | tiene   | aprobado   | 30%          |
