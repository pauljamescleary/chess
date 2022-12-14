from flask import abort, request, session
from chess.models import *
from chess.schemas import *
from sqlalchemy.exc import IntegrityError


def configure_routes(app, db, pwd_context, auth):

    @auth.verify_password
    def verify_password(email, password):
        user = db.session.query(User).filter(User.email == email).one_or_none()
        if user and pwd_context.verify(password, user.password):
            return user

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

    @app.route("/user", methods=['GET'])
    @auth.login_required
    def get_user():
        # Hide the password
        user = auth.current_user()
        user.password = None
        return user_schema.dump(user)        

    @app.route("/scores", methods=['POST'])
    @auth.login_required
    def save_score():
        # Get the user id from the session cookie
        user_id = auth.current_user().id

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

    @app.route("/scores/top", methods=['GET'])
    @auth.login_required
    def high_score():
        user_id = auth.current_user().id

        if user_id:
            score = db.session.query(Score).filter(Score.user_id == user_id).order_by(
                Score.score.desc()).limit(1).one_or_none()
            return score_schema.dump(score)
        else:
            abort(401)
