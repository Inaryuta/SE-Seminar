import requests
from behave import given, when, then

API_URL = "http://localhost:8000"

@given('the user has an ID of 1')
def step_given_user_id(context):
    context.user_id = 1

@when('I am sending a GET request to "/routine-sessions?user_id=1"')
def step_send_get_request(context):
    response = requests.get(f"{API_URL}/routine-sessions", params={"user_id": context.user_id})
    context.response = response

@then('the response should contain the user sessions')
def step_verify_response_contains_sessions(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert isinstance(data, list)
    assert len(data) > 0
