import datetime
import json
import base64
import requests
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .BaseClass import *
from System import session
from sqlalchemy import Date

class UsersClass(Base):
    __tablename__ = 'users'

    id_user: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    id_user_group: Mapped[str] = mapped_column()
    sha1: Mapped[str] = mapped_column()

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "username": self.username,
            "email": self.email,
            "id_user_group": self.id_user_group,
            "sha1": self.sha1,
        }

    @classmethod
    def add(cls, _username, _password, _email, _id_user_group, _sha1):

        record = cls(
            username=_username,
            password=_password,
            email=_email,
            id_user_group=_id_user_group,
            sha1=_sha1
        )
        session.add(record)
        session.commit()

    @classmethod
    def get_all(cls):
        records = session.query(cls).all()
        return [record.to_dict() for record in records]

    @classmethod
    def get_by_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def get(cls, id_user):
        return session.query(cls).filter_by(id_user=id_user).first()


    @classmethod
    def validate_password(cls, username, password):
        user = cls.get_by_username(username)
        if user and user.password == password:
            return True  # Password is correct
        return False  # Password is incorrect
