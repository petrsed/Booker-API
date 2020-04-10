import sqlalchemy
from data.db_session import SqlAlchemyBase


class UserType(SqlAlchemyBase):
    __tablename__ = 'user_types'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
