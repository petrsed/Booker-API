import sqlalchemy
from data.db_session import SqlAlchemyBase


class IssueTypes(SqlAlchemyBase):
    __tablename__ = 'issue_types'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
