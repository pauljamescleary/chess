import pytest
import uuid
import base64

# client comes from pytest-flask


def test_create_user(client, sample_user):
    uid = uuid.uuid4()
    user = {"email": f"foo{uid}@test.com", "password": "password"}
    resp = client.post('/users', json=user)
    assert resp.status_code == 200


def test_get_users(client, sample_user):
    resp = client.get('/users')
    assert resp.status_code == 200
    users = resp.json
    # we should have our sample user in there
    user_emails = list(map(lambda x: x['email'], users))
    assert sample_user.email in user_emails

def test_high_score(client, sample_user):
    score = { "score": 100, "level": 1}
    auth_string = f"{sample_user.email}:password"
    auth_ascii = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_ascii)
    auth = { 'Authorization': "Basic " + auth_b64.decode('ascii') }
    resp = client.post('/scores', headers=auth, json=score)
    assert resp.status_code == 200
