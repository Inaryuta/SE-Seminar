Feature: Filter training sessions by user and date range

  Scenario: Filter sessions for a user between two dates
    Given a user with ID 1
    When I send a GET request to "/routine-sessions/sessions/filter?user_id=1&start_date=2025-07-30&end_date=2025-08-01"
    Then the response should contain a list of filtered sessions
