import pytest
import flask_migrate
import chess
from chess.models import User
from chess import password_hasher
from chess import db as _db


@pytest.fixture(scope="session")
def app():
    app = chess.create_app(env='test')
    with app.app_context():
        flask_migrate.upgrade()
    return app

@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()

@pytest.fixture
def sample_user(db):
    user = User(email='test@test.com', password=password_hasher.hash("password"))
    db.session.add(user)
    db.session.commit()

    return user
