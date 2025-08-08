import requests
from behave import given, when, then

API_URL = "http://localhost:8000"

@given('the user with ID 1 has multiple routine sessions')
def step_impl_given_user_sessions(context):
    context.user_id = 1

@when('I send a GET request to "/routine-sessions?user_id=1"')
def step_impl_send_request(context):
    response = requests.get(f"{API_URL}/routine-sessions", params={"user_id": context.user_id})
    context.response = response
    context.json = response.json()

@then('the response should have status code 200')
def step_impl_status_code(context):
    assert context.response.status_code == 200



@then('the response should have enough data to calculate statistics')
def step_validate_stats_data(context):
    response_data = context.response.json()
    assert isinstance(response_data, list), "Expected a list of sessions"

    assert len(response_data) >= 5, "Expected at least 5 sessions to calculate statistics"

    for session in response_data:
        assert 'duration_minutes' in session, "Missing 'duration_minutes' in session"
        assert 'calories_burned' in session, "Missing 'calories_burned' in session"
        assert isinstance(session['duration_minutes'], (int, float)), "'duration_minutes' must be numeric"
        assert isinstance(session['calories_burned'], (int, float)), "'calories_burned' must be numeric"
