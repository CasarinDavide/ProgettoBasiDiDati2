from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base, BaseUser
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

## TODO ##