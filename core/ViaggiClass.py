from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

"""
CREATE TABLE dev.Viaggi (
                            id_viaggio SERIAL PRIMARY KEY,
                            durata INTEGER NOT NULL,
                            id_aereoporto_partenza VARCHAR(200) REFERENCES dev.Aereoporti(id_aereoporto) ON DELETE SET NULL,
                            id_aereoporto_arrivo VARHCAR(200) REFERENCES dev.Aereoporti(id_aereoporto) ON DELETE SET NULL,
                            sconto_biglietto REAL NOT NULL
                            data_partenza DATE,
                            orario_partenza TIME
);
"""
class ViaggiClass(Base):
    __tablename__ = 'Viaggi'
    __table_args__ = { 'schema': 'dev' }

    id_viaggio: Mapped[int] = mapped_column(primary_key=True)
    durata: Mapped[int] = mapped_column(nullable=False)
    sconto_biglietto: Mapped[float] = mapped_column(nullable=False)
    data_partenza: Mapped[datetime] = mapped_column(nullable=True)
    orario_partenza: Mapped[datetime] = mapped_column(nullable=True)

    
    # FK -> Aereoporto Partenza
    id_aereoporto_partenza: Mapped[str] = mapped_column(ForeignKey('dev.Aereoporti.id_aereoporto'), nullable=False)
    partenza_rel = relationship('AereoportiClass', foreign_keys=[id_aereoporto_partenza],back_populates='viaggi_partenza_rel')
    
    # FK -> Aereoporto Arrivo
    id_aereoporto_arrivo: Mapped[str] = mapped_column(ForeignKey('dev.Aereoporti.id_aereoporto'), nullable=False)
    arrivo_rel = relationship('AereoportiClass', foreign_keys=[id_aereoporto_arrivo],back_populates='viaggi_arrivo_rel')

    #Biglietti associati al viaggio
    biglietti_rel = relationship('BigliettiClass', back_populates='viaggio_rel')

    #Voli che compongono il viaggio
    voli_rel = relationship('VoliClass', back_populates='viaggio_rel')

    #Compagnie che compongono il viaggio
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id_compagnia'),nullable=False)
    compagnia_rel = relationship('CompagnieClass', back_populates='viaggi_rel')