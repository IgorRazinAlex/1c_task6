import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase

from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Dinner(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "dinners"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    meal_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"))
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now())
