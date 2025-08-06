Feature: Register Training Session

  Scenario: Successful session registration
    Given a registered user with a routine
    And I have valid session data
    When I send the session registration request
    Then I receive a successful session registration response

  Scenario: Session registration with missing duration
    Given a registered user with a routine
    And I have incomplete session data
    When I send the incomplete session registration request
    Then I receive an error response indicating validation failure
