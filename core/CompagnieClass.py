from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin
"""
CREATE TABLE dev.Compagnie (
                               id_compagnia SERIAL PRIMARY KEY,
                               email VARCHAR(200) UNIQUE NOT NULL,
                               password VARCHAR(255) NOT NULL,
                               tel VARCHAR(20) NOT NULL,
                               nome VARCHAR(200) NOT NULL,
                               via VARCHAR(200) NOT NULL,
                                civico VARCHAR(200) NOT NULL,
                                cod_postale INTEGER NOT NULL,
                                citta VARCHAR(200) NOT NULL,
                                paese VARCHAR(200) NOT NULL
);
"""



class CompagnieClass(UserMixin, Base):
    __tablename__ = 'Compagnie'
    __table_args__ = { 'schema': 'dev' }


    id_compagnia: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)

    via: Mapped[str] = mapped_column(nullable=False)
    civico: Mapped[str] = mapped_column(nullable=False)
    cod_postale: Mapped[int] = mapped_column(nullable=False)
    citta: Mapped[str] = mapped_column(nullable=False)
    paese: Mapped[str] = mapped_column(nullable=False)

    #Dipendenti della compagnia
    dipendenti_rel = relationship('DipendentiClass', back_populates='compagnia_rel')

    #Aerei associati alla compagnia
    aerei_rel = relationship('AereiClass', back_populates='compagnia_rel')

    #Viaggi effettuati dalla compagnia
    effettuano_rel = relationship('EffettuanoClass', back_populates='compagnia_rel')


    def get_id(self):
        return str(self.id_compagnia)

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_role(self):
        return "compagnie"