import sqlalchemy
from data.db_session import SqlAlchemyBase


class Books(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    barcode = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)