from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

class DipendentiClass(UserMixin, Base):
    __tablename__ = 'Dipendenti'
    __table_args__ = { 'schema': 'dev' }
    

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    ruolo: Mapped[str] = mapped_column(nullable=False)
    # FK -> Compagnie
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id'), nullable=False)
    compagnia_rel = relationship('CompagnieClass', back_populates='dipendenti_rel')
