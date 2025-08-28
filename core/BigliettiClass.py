import enum

from System import Base
from typing import Literal    
from sqlalchemy import ForeignKey
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
"""
CREATE TABLE dev.Biglietti (
                               id_biglietto VARCHAR(200) PRIMARY KEY,
                               categoria classe NOT NULL,
                               prezzo REAL NOT NULL,
                               posto VARCHAR(4) NOT NULL,
                               id_viaggio INTEGER REFERENCES dev.Viaggi(id_viaggio) ON DELETE CASCADE,
                               id_passeggero INTEGER REFERENCES dev.Passeggeri(id_passeggero) ON DELETE CASCADE
);
"""

class CategoriaEnum(str, enum.Enum):
    Economy = "Economy"
    Business = "Business"
    FirstClass = "FirstClass"

class BigliettiClass(Base):
    __tablename__ = 'Biglietti'
    __table_args__ = { 'schema': 'dev' }

    id_biglietto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    categoria: Mapped[CategoriaEnum] = mapped_column(Enum(CategoriaEnum, name="classe"), nullable=False)
    prezzo: Mapped[float] = mapped_column(nullable=False)
    posto: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    id_volo: Mapped[int] = mapped_column(nullable=False)
    internet: Mapped[int] = mapped_column(nullable=False)
    snack: Mapped[int] = mapped_column(nullable=False)
    bagagli: Mapped[int] = mapped_column(nullable=False)

    # FK -> Viaggi
    id_viaggio = mapped_column(ForeignKey('dev.Viaggi.id_viaggio'), nullable=False)
    viaggio_rel = relationship('ViaggiClass', back_populates='biglietti_rel')
    
    # FK -> Passeggeri
    id_passeggero = mapped_column(ForeignKey('dev.Passeggeri.id_passeggero'), nullable=True)
    passeggero_rel = relationship('PasseggeriClass', back_populates='biglietti_rel')

    id_volo = mapped_column(ForeignKey('dev.Voli.id_volo'), nullable=False)
    volo_rel = relationship('VoliClass', back_populates='biglietti_rel')

