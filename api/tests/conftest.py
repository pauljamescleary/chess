import pytest
import flask_migrate
import chess
from chess import db as _db
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def app():
    load_dotenv()
    app = chess.create_app()
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
