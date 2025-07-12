from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

class CompagnieClass(UserMixin, Base):
    __tablename__ = 'Compagnie'
    __table_args__ = { 'schema': 'dev' }


    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    # FK -> Address
    address_id: Mapped[int] = mapped_column(ForeignKey('dev.Indirizzi.id'), nullable=False)

    #Indirizzo della Compagnia
    address_rel = relationship('IndirizziClass', back_populates='compagnia_rel')

    #Dipendenti della compagnia
    dipendenti_rel = relationship('DipendentiClass', back_populates='compagnia_rel')

    #Aerei associati alla compagnia
    aerei_rel = relationship('AereiClass', back_populates='compagnia_rel')

    #Viaggi effettuati dalla compagnia
    effettuano_rel = relationship('EffettuanoClass', back_populates='compagnia_rel')