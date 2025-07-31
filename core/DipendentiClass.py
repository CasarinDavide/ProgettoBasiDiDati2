from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

"""
CREATE TABLE dev.Dipendenti (
                                id_dipendente SERIAL PRIMARY KEY,
                                email VARCHAR(200) UNIQUE NOT NULL,
                                password VARCHAR(255) NOT NULL,
                                tel VARCHAR(20) NOT NULL,
                                nome VARCHAR(200) NOT NULL,
                                cognome VARCHAR(200) NOT NULL,
                                ruolo VARCHAR(200) NOT NULL,
                                id_compagnia INTEGER REFERENCES dev.Compagnie(id_compagnie) ON DELETE SET NULL
);
"""
class DipendentiClass(UserMixin, Base):
    __tablename__ = 'Dipendenti'
    __table_args__ = { 'schema': 'dev' }


    id_dipendente: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    ruolo: Mapped[str] = mapped_column(nullable=False)
    # FK -> Compagnie
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id_compagnia'), nullable=False)
    compagnia_rel = relationship('CompagnieClass', back_populates='dipendenti_rel')

    def get_id(self):
        return str(self.id_dipendente)

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_role(self):
        return "compagnie"
