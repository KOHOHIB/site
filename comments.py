import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    theme_id = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    owner_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)