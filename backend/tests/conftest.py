import pytest

@pytest.fixture(scope="session")
def app():
    # set env vars
    import os
    os.environ['FLASK_SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['FLASK_SECRET_KEY'] = 'fortesting'
    os.environ['FLASK_DEBUG'] = '1'
    from chess import app
    return app

@pytest.fixture
def sample_user():
    from chess import password_hasher
    from chess import db
    from chess.models import User

    try:
        user = User(email='test@test.com', password=password_hasher.hash("password"))
        db.session.add(user)
        db.session.commit()
    except:
        # This happened because of a unique constraint
        db.session.rollback()
        pass

    return user
