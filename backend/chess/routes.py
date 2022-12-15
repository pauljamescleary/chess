from flask import abort, jsonify, request
from sqlalchemy.exc import IntegrityError

from chess.models import Score, User
from chess import app, db, password_hasher, auth

@auth.verify_password
def verify_password(email, password):
    print('VERIFYING USER...')
    user = db.session.query(User).filter(User.email == email).one_or_none()
    if user and password_hasher.verify(password, user.password):
        return user
    elif user:
        print('USER FOUND, PASSWORD INCORRECT?')
    else:
        print('USER NOT FOUND!!!')

@app.before_request
def before_request():
    print("*** BEFORE REQUEST***")
    print(request.method, request.endpoint, request.authorization)

    try:
        request_js = request.data
        if request_js:
            print(request_js)
        else:
            print('NO DATA?')
    except Exception as err:
        print(err)

@app.route("/users", methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return jsonify(users)

@app.route("/users", methods=['POST'])
def create_user():
    # Assumes the user passes in json like { "email": "x", "password": "y"}
    email = request.json.get('email')
    password = request.json.get('password')
    user = User(email=email, password=password_hasher.hash(password))

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        print("Duplicate create user, is ok...")

    return jsonify(user)

@app.route("/user", methods=['GET'])
@auth.login_required
def get_user():
    # Hide the password
    user = auth.current_user()
    user.password = None
    return jsonify(user)

@app.route("/scores", methods=['POST'])
@auth.login_required
def save_score():
    # Get the user id from the session cookie
    user_email = auth.current_user().email

    if user_email:
        score = request.json.get('score')
        level = request.json.get('level')

        s = Score(score=score, level=level, user_email=user_email)
        db.session.add(s)
        db.session.commit()

        return jsonify(s)
    else:
        print("Unable to save score, no user session found")
        abort(401)

@app.route("/scores/top", methods=['GET'])
@auth.login_required
def high_score():
    user_email = auth.current_user().email

    if user_email:
        score = db.session.query(Score).where(Score.user_email == user_email).order_by(
            Score.score.desc()).limit(1).one_or_none()
        return jsonify(score)
    else:
        abort(401)
