Feature: Estadísticas de entrenamiento del usuario

  Scenario: Calcular estadísticas a partir del historial de sesiones
    Given the user with ID 1 has multiple routine sessions
    When I send a GET request to "/routine-sessions?user_id=1"
    Then the response should have status code 200
    And the response should contain a list of sessions
    And the response should have enough data to calculate statistics
