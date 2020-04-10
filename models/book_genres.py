import sqlalchemy
from data.db_session import SqlAlchemyBase

class BookGenre(SqlAlchemyBase):
    __tablename__ = 'book_genre'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
