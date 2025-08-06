import requests
from behave import given, when, then
from datetime import datetime
import uuid

API_URL = "http://localhost:8000"

@given("a registered user with a routine")
def step_impl(context):
    # Crear un usuario único
    unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    user_payload = {
        "username": "session_user",
        "email": unique_email,
        "password": "password123"
    }
    user_response = requests.post(f"{API_URL}/auth/register", json=user_payload)
    assert user_response.status_code == 200, f"User creation failed: {user_response.text}"
    user_data = user_response.json()
    context.user_id = user_data["id"]

    # Crear una rutina asociada a ese usuario
    routine_payload = {
        "name": "Test Routine",
        "description": "Routine for testing",
        "user_id": context.user_id
    }
    routine_response = requests.post(f"{API_URL}/routines/", json=routine_payload)
    assert routine_response.status_code == 200, f"Routine creation failed: {routine_response.text}"
    context.routine_id = routine_response.json()["id"]

@given("I have valid session data")
def step_impl(context):
    context.session_data = {
        "user_id": context.user_id,
        "routine_id": context.routine_id,
        "date": datetime.now().isoformat(),
        "duration_minutes": 45,
        "session_intensity": "High",
        "calories_burned": 400.0
    }

@when("I send the session registration request")
def step_impl(context):
    context.response = requests.post(f"{API_URL}/routine-sessions/", json=context.session_data)

@then("I receive a successful session registration response")
def step_impl(context):
    print("DEBUG RESPONSE:", context.response.status_code, context.response.text)
    assert context.response.status_code == 200, "Expected 200 OK for successful registration"
    data = context.response.json()
    assert data["user_id"] == context.session_data["user_id"]
    assert data["routine_id"] == context.session_data["routine_id"]
    assert data["duration_minutes"] == context.session_data["duration_minutes"]
    assert data["session_intensity"] == context.session_data["session_intensity"]
    assert data["calories_burned"] == context.session_data["calories_burned"]

@given("I have incomplete session data")
def step_impl(context):
    context.session_data = {
        "user_id": context.user_id,
        "routine_id": context.routine_id,
        "date": datetime.now().isoformat(),
        # Falta duration_minutes
        "session_intensity": "Medium",
        "calories_burned": 250.0
    }

@when("I send the incomplete session registration request")
def step_impl(context):
    context.response = requests.post(f"{API_URL}/routine-sessions/", json=context.session_data)

@then("I receive an error response indicating validation failure")
def step_impl(context):
    print("DEBUG ERROR RESPONSE:", context.response.status_code, context.response.text)
    assert context.response.status_code == 422 or context.response.status_code == 400
