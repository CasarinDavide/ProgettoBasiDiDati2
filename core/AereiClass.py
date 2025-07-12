from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AereiClass(Base):
    __tablename__ = 'Aerei'
    __table_args__ = { 'schema': 'dev' }

    id: Mapped[int] = mapped_column(primary_key=True)
    capacita: Mapped[int] = mapped_column(nullable=False)
    modello: Mapped[str] = mapped_column(nullable=False)
    consumoMedio: Mapped[float] = mapped_column(nullable=False)
    dimensione: Mapped[str] = mapped_column(nullable=False)
    # FK -> Compagnie
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id'), nullable=False)
    compagnia_rel = relationship('CompagnieClass', back_populates='aerei_rel')

    # Voli effettuati dall'aereo
    voli_rel = relationship('VoliClass', back_populates='aereo_rel')
