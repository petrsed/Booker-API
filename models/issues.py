import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Issues(SqlAlchemyBase):
    __tablename__ = 'issues'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, index=True)
    book_id = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
