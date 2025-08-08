Feature: Retrieve training session history

  Scenario: User retrieves their session history
    Given the user has registered sessions with user_id 1
    When I make a GET request to "/routine-sessions?user_id=1"
    Then the response status code should be 200
    And the response should contain a list of sessions
