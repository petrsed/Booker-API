import sqlalchemy
from data.db_session import SqlAlchemyBase


class Image(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    url = sqlalchemy.Column(sqlalchemy.String)
