from config import app, db, pwd_context
from flask import request, session
from models import *
from schemas import *
from sqlalchemy.exc import IntegrityError

@app.route("/users", methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    return users_schema.dump(users)


@app.route("/users", methods=['POST'])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User(email=email, password=pwd_context.hash(password))

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        print("Duplicate, is ok...")

    return user_schema.dump(user)

@app.route("/login", methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = db.session.query(User).filter(User.email == email).one_or_none()
    if user:
        if pwd_context.verify(password, user.password):
            session['user_id'] = user.id
            return "LOGIN SUCCESS"
        else:
            return "LOGIN FAILED, INVALID PASSWORD"
    else:
        return "LOGIN FAILED"

@app.route("/login", methods=['DELETE'])
def logout():
    session.pop('user_id')
    return 'SESSION DELETED'    

# TODO: This must pull the id from the current session
@app.route("/users/scores", methods=['POST'])
def save_score():
    user_id = session.get('user_id')

    if user_id:
        score = request.json.get('score')
        level = request.json.get('level')

        s = Score(score=score, level=level, user_id=user_id)
        db.session.add(s)
        db.session.commit()

        return score_schema.dump(s)
    else:
        return "NO SESSION FOUND, PLEASE LOGIN"

@app.route("/users/scores/top", methods=['GET'])
def high_score():
    user_id = session.get('user_id')

    if user_id:
        score = db.session.query(Score).filter(Score.user_id == user_id).order_by(Score.score.desc()).limit(1).one_or_none()
        return score_schema.dump(score)
    else:
        return "NO SESSION FOUND, PLEASE LOGIN"

if __name__ == '__main__':
    do_init()
    app.run(debug=True, host='0.0.0.0')
