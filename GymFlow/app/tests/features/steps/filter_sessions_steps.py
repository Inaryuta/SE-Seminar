import requests
from behave import given, when, then

BASE_URL = "http://localhost:8000"

@given('a user with ID 1')
def step_given_user(context):
    context.user_id = 1

@when('I send a GET request to "/routine-sessions/sessions/filter?user_id=1&start_date=2025-07-30&end_date=2025-08-01"')
def step_when_get_filtered_sessions(context):
    url = f"{BASE_URL}/routine-sessions/sessions/filter?user_id=1&start_date=2025-07-30&end_date=2025-08-01"
    response = requests.get(url)
    context.response = response

@then('the response should contain a list of filtered sessions')
def step_then_check_filtered_sessions(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert isinstance(data, list)
