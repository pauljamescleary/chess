from flask import url_for
from chess import password_hasher
import pytest
import uuid

# client comes from pytest-flask
def test_create_user(client):
    uid = uuid.uuid4()
    url = url_for('create_user')
    user = {"email": f"foo{uid}@test.com", "password": "password"}
    resp = client.post(url, json=user)
    assert resp.status_code == 200
