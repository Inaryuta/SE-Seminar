Feature: User Registration and Login

  Scenario: Successful user registration
    Given I am a new user
    When I send a registration request with valid username, email and password
    Then I receive a successful registration response

  Scenario: Register with existing email
    Given I am a new user with an email that already exists
    When I send a registration request
    Then I receive an error response indicating the email is already in use

  Scenario: Successful user login
    Given I am a registered user
    When I send a login request with correct credentials
    Then I receive a successful login response

  Scenario: Login with incorrect password
    Given I am a registered user
    When I send a login request with an incorrect password
    Then I receive an error response indicating invalid credentials
