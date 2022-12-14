from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from chess.models import User, Score

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class ScoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Score
        include_fk = True
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
score_schema = ScoreSchema()
scores_schema = ScoreSchema(many=True)
