Feature: View session history
  As a user
  I want to view my workout session history
  So that I can track my training progress

  Scenario: User views session history
    Given the user has an ID of 1
    When I am sending a GET request to "/routine-sessions?user_id=1"
    Then the response should contain the user sessions

