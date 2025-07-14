from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin
"""
CREATE TABLE dev.Compagnie (
                               id_compagnie SERIAL PRIMARY KEY,
                               email VARCHAR(200) UNIQUE NOT NULL,
                               password VARCHAR(255) NOT NULL,
                               tel VARCHAR(20) NOT NULL,
                               nome VARCHAR(200) NOT NULL,
                               address_id INTEGER REFERENCES dev.Indirizzi(address_id) ON DELETE SET NULL
);
"""



class CompagnieClass(UserMixin, Base):
    __tablename__ = 'Compagnie'
    __table_args__ = { 'schema': 'dev' }


    id_compagnie: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    # FK -> Address
    address_id: Mapped[int] = mapped_column(ForeignKey('dev.Indirizzi.address_id'), nullable=False)

    #Indirizzo della Compagnia
    address_rel = relationship('IndirizziClass', back_populates='compagnia_rel')

    #Dipendenti della compagnia
    dipendenti_rel = relationship('DipendentiClass', back_populates='compagnia_rel')

    #Aerei associati alla compagnia
    aerei_rel = relationship('AereiClass', back_populates='compagnia_rel')

    #Viaggi effettuati dalla compagnia
    effettuano_rel = relationship('EffettuanoClass', back_populates='compagnia_rel')




