from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

def engine():
    load_dotenv()
    # Create SQLAlchemy engine globally
    return create_engine(os.getenv('URL'))

class Base(DeclarativeBase):
    pass