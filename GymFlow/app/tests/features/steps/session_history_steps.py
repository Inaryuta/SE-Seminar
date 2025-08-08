from behave import given, when, then
import requests

API_URL = "http://localhost:8000"

@given('the user has registered sessions with user_id 1')
def step_impl_given_user_has_sessions(context):
    # Opcional: podrías insertar datos si no existen aún
    context.user_id = 1

@when('I make a GET request to "/routine-sessions?user_id=1"')
def step_impl_when_make_request(context):
    response = requests.get(f"{API_URL}/routine-sessions", params={"user_id": context.user_id})
    context.response = response

@then('the response status code should be 200')
def step_impl_then_status_code(context):
    assert context.response.status_code == 200

@then('the response should contain a list of sessions')
def step_impl_then_check_sessions(context):
    data = context.response.json()
    assert isinstance(data, list)
