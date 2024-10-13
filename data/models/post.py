import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))
    calories = sqlalchemy.Column(sqlalchemy.Float, default=0)
    proteins = sqlalchemy.Column(sqlalchemy.Float, default=0)
    fats = sqlalchemy.Column(sqlalchemy.Float, default=0)
    carbonades = sqlalchemy.Column(sqlalchemy.Float, default=0)
    update_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now())
    about = sqlalchemy.Column(sqlalchemy.String)
