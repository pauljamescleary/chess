import pytest
import uuid

# client comes from pytest-flask


def test_create_user(client, sample_user):
    uid = uuid.uuid4()
    user = {"email": f"foo{uid}@test.com", "password": "password"}
    resp = client.post('/users', json=user)
    assert resp.status_code == 200


def test_login(client, sample_user):
    user = {"email": sample_user.email, "password": "password"}
    resp = client.post('/login', json=user)
    assert resp.status_code == 200

    # Find the session cookie, should be present
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "session"), None)
    assert cookie is not None


def test_logout(client, sample_user):
    user = {"email": sample_user.email, "password": "password"}
    resp = client.post('/login', json=user)
    assert resp.status_code == 200

    # Find the session cookie, should be present
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "session"), None)
    assert cookie is not None

    # Logout
    resp = client.delete('/login')
    assert resp.status_code == 200
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "session"), None)
    assert cookie is None


def test_get_users(client, sample_user):
    resp = client.get('/users')
    assert resp.status_code == 200
    users = resp.json
    # we should have our sample user in there
    user_emails = list(map(lambda x: x['email'], users))
    assert sample_user.email in user_emails
