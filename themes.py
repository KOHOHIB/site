import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Themes(SqlAlchemyBase):
    __tablename__ = 'theme'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    owner_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)