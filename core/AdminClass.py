from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base, BaseUser
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
"""

"""



class AdminClass(BaseUser, Base):
    __tablename__ = 'Admin'
    __table_args__ = { 'schema': 'dev' }


    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)

    def get_id(self):
        return str(self.id)

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_role(self):
        return "admin"

