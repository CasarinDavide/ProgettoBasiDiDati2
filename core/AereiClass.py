from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
CREATE TABLE dev.Aerei (
                           id_aerei SERIAL PRIMARY KEY,
                           capacita INT NOT NULL,
                           modello VARCHAR(200) NOT NULL,
                           consumoMedio REAL NOT NULL,
                           dimensione VARCHAR(200) NOT NULL,
                           id_compagnia INTEGER REFERENCES dev.Compagnie(id_compagnie) ON DELETE CASCADE
);
"""
class AereiClass(Base):
    __tablename__ = 'Aerei'
    __table_args__ = { 'schema': 'dev' }

    id_aerei: Mapped[int] = mapped_column(primary_key=True)
    capacita: Mapped[int] = mapped_column(nullable=False)
    modello: Mapped[str] = mapped_column(nullable=False)
    consumoMedio: Mapped[float] = mapped_column(nullable=False)
    dimensione: Mapped[str] = mapped_column(nullable=False)
    # FK -> Compagnie
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id_compagnie'), nullable=False)
    compagnia_rel = relationship('CompagnieClass', back_populates='aerei_rel')

    # Voli effettuati dall'aereo
    voli_rel = relationship('VoliClass', back_populates='aereo_rel')
