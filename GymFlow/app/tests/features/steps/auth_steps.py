import requests
import json
from behave import given, when, then
import uuid


API_URL = "http://localhost:8000"

@given("I am a new user")
def step_impl(context):
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    context.user_data = {
        "username": "testuser123",
        "email": unique_email,
        "password": "securepassword"
    }


@given("I am a new user with an email that already exists")
def step_impl(context):
    existing_email = "existing@example.com"
    context.user_data = {
        "username": "anotheruser",
        "email": existing_email,
        "password": "password123"
    }
    # Register the user first if not already created
    requests.post(f"{API_URL}/auth/register", json=context.user_data)

@when("I send a registration request with valid username, email and password")
@when("I send a registration request")
def step_impl(context):
    response = requests.post(f"{API_URL}/auth/register", json=context.user_data)
    context.response = response

@then("I receive a successful registration response")
def step_impl(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert data["email"] == context.user_data["email"]

@then("I receive an error response indicating the email is already in use")
def step_impl(context):
    assert context.response.status_code == 400
    error_message = context.response.json()["detail"].lower()
    assert "ya está registrado" in error_message


@given("I am a registered user")
def step_impl(context):
    context.login_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "mypassword"
    }
    # Register the user
    requests.post(f"{API_URL}/auth/register", json=context.login_data)

@when("I send a login request with correct credentials")
def step_impl(context):
    login_payload = {
        "email": context.login_data["email"],
        "password": context.login_data["password"]
    }
    context.response = requests.post(f"{API_URL}/auth/login", json=login_payload)

@then("I receive a successful login response")
def step_impl(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert data["email"] == context.login_data["email"]

@when("I send a login request with an incorrect password")
def step_impl(context):
    login_payload = {
        "email": context.login_data["email"],
        "password": "wrongpassword"
    }
    context.response = requests.post(f"{API_URL}/auth/login", json=login_payload)

@then("I receive an error response indicating invalid credentials")
def step_impl(context):
    assert context.response.status_code == 401
    error_message = context.response.json()["detail"].lower()
    assert "contraseña incorrecta" in error_message
