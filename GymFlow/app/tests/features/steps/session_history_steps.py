import requests
from behave import given, when, then
from datetime import datetime

API_URL = "http://localhost:8000"

@given("I am an existing user with training sessions")
def step_impl(context):
    context.user_data = {
        "username": "historyuser",
        "email": "historyuser@example.com",
        "password": "securepass"
    }

    # Registro del usuario
    response = requests.post(f"{API_URL}/auth/register", json=context.user_data)
    if response.status_code == 400 and "ya está registrado" in response.text:
        pass  # El usuario ya existe
    else:
        assert response.status_code == 200

    context.user_id = response.json().get("id", 1)  # por si ya existía

    # Crear una rutina
    routine_data = {
        "name": "Routine for History",
        "description": "Test routine",
        "user_id": context.user_id
    }
    routine_response = requests.post(f"{API_URL}/routines/", json=routine_data)
    assert routine_response.status_code == 200
    context.routine_id = routine_response.json()["id"]

    # Crear sesiones
    for i in range(2):
        session_data = {
            "user_id": context.user_id,
            "routine_id": context.routine_id,
            "date": datetime.now().isoformat(),
            "duration_minutes": 30 + i * 10,
            "session_intensity": "Medium",
            "calories_burned": 250.0 + i * 50
        }
        response = requests.post(f"{API_URL}/routine-sessions/", json=session_data)
        assert response.status_code == 200

@given("I am an existing user with no training sessions")
def step_impl(context):
    context.user_data = {
        "username": "nosessions",
        "email": "nosessions@example.com",
        "password": "securepass"
    }

    # Registrar usuario sin sesiones
    response = requests.post(f"{API_URL}/auth/register", json=context.user_data)
    if response.status_code == 400 and "ya está registrado" in response.text:
        pass
    else:
        assert response.status_code == 200

    context.user_id = response.json().get("id", 2)

@when("I request my training session history")
def step_impl(context):
    response = requests.get(f"{API_URL}/routine-sessions/")
    context.session_history_response = response
    try:
        print("DEBUG HISTORY RESPONSE:", response.status_code, response.json())
    except Exception as e:
        print("DEBUG HISTORY RAW RESPONSE:", response.status_code, response.text)
        raise e


@then("I receive a list of my past training sessions")
def step_impl(context):
    response = context.session_history_response
    assert response.status_code == 200
    sessions = response.json()
    assert isinstance(sessions, list)
    assert len(sessions) > 0

@then("I receive an empty list")
def step_impl(context):
    response = context.session_history_response
    assert response.status_code == 200
    assert response.json() == []
