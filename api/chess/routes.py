from flask import abort, request, session
from chess.models import *
from chess.schemas import *
from sqlalchemy.exc import IntegrityError


def configure_routes(app, db, pwd_context):

    @app.route("/users", methods=['GET'])
    def get_users():
        users = db.session.query(User).all()
        return users_schema.dump(users)

    @app.route("/users", methods=['POST'])
    def create_user():
        # Assumes the user passes in json like { "email": "x", "password": "y"}
        email = request.json.get('email')
        password = request.json.get('password')
        user = User(email=email, password=pwd_context.hash(password))

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            print("Duplicate create user, is ok...")

        return user_schema.dump(user)

    @app.route("/login", methods=['POST'])
    def login():
        # Assumes the user passes in json like { "email": "x", "password": "y"}
        email = request.json.get('email')
        password = request.json.get('password')

        # First, we attempt to find the user from the database
        # Possible that the user does not exist
        user = db.session.query(User).filter(User.email == email).one_or_none()
        if user:
            # Verify that the password provided matches the hashed password
            # from the database
            if pwd_context.verify(password, user.password):
                # Create a session with the user_id and return 200 OK
                session['user_id'] = user.id
                return 'OK'
            else:
                # Password didn't match, abort with a 401
                print(f"Password provided for user {email} did not match")
                abort(401)
        else:
            # User was not found
            abort(401)

    @app.route("/login", methods=['DELETE'])
    def logout():
        # Remove the session cookie        
        session.pop('user_id')        
        return 'OK'

    @app.route("/users/scores", methods=['POST'])
    def save_score():
        # Get the user id from the session cookie
        user_id = session.get('user_id')

        if user_id:
            score = request.json.get('score')
            level = request.json.get('level')

            s = Score(score=score, level=level, user_id=user_id)
            db.session.add(s)
            db.session.commit()

            return score_schema.dump(s)
        else:
            print("Unable to save score, no user session found")
            abort(401)

    @app.route("/users/scores/top", methods=['GET'])
    def high_score():
        user_id = session.get('user_id')

        if user_id:
            score = db.session.query(Score).filter(Score.user_id == user_id).order_by(
                Score.score.desc()).limit(1).one_or_none()
            return score_schema.dump(score)
        else:
            abort(401)
