from flask import request
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

SNACK_PRICE = 5
INTERNET_PRICE = 10
BAGAGLIO_PRICE = 20

def engine():
    load_dotenv()
    # Create SQLAlchemy engine globally
    return create_engine(os.getenv('URL'))

class Base(DeclarativeBase):
    pass

def getParam(param: str):
    merged_params = request.args.to_dict() | request.form.to_dict()
    return merged_params.get(param)


class BaseUser(UserMixin):
    def __init__(self, id = "", nome= "", email= "", role= "",**kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.nome = nome
        self.email = email
        self.role = role

    def get_id(self):
        return f"{self.role}-{self.id}"


