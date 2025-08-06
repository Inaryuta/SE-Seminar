Feature: View Training Session History

  Scenario: User views full training session history
    Given I am an existing user with training sessions
    When I request my training session history
    Then I receive a list of my past training sessions

  Scenario: User with no sessions views training history
    Given I am an existing user with no training sessions
    When I request my training session history
    Then I receive an empty list
