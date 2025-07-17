from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
CREATE TABLE dev.Viaggi (
                            id_viaggio SERIAL PRIMARY KEY,
                            sosta INTEGER NOT NULL,
                            durata INTEGER NOT NULL,
                            id_aereoporto_partenza INTEGER REFERENCES dev.Aereoporti(id_aereoporto) ON DELETE SET NULL,
                            id_aereoporto_arrivo INTEGER REFERENCES dev.Aereoporti(id_aereoporto) ON DELETE SET NULL,
                            sconto_biglietto REAL NOT NULL
);
"""
class ViaggiClass(Base):
    __tablename__ = 'Viaggi'
    __table_args__ = { 'schema': 'dev' }

    id_viaggio: Mapped[int] = mapped_column(primary_key=True)
    sosta: Mapped[int] = mapped_column(nullable=False)
    durata: Mapped[int] = mapped_column(nullable=False)
    sconto: Mapped[float] = mapped_column(nullable=False)
    ordine: Mapped[int] = mapped_column(nullable=False)
    
    # FK -> Aereoporto Partenza
    id_aereoporto_partenza: Mapped[int] = mapped_column(ForeignKey('dev.Aereoporti.id_aereoporto'), nullable=False)
    partenza_rel = relationship('AereoportiClass', foreign_keys=[id_aereoporto_partenza],back_populates='viaggi_partenza_rel')
    
    # FK -> Aereoporto Arrivo
    id_aereoporto_arrivo: Mapped[int] = mapped_column(ForeignKey('dev.Aereoporti.id_aereoporto'), nullable=False)
    arrivo_rel = relationship('AereoportiClass', foreign_keys=[id_aereoporto_arrivo],back_populates='viaggi_arrivo_rel')

    #Date di partenza associate al viaggio
    data_partenze_rel = relationship('DataPartenzeClass', back_populates='viaggio_rel')

    #Compagnie Aree che effettuano questo viaggio
    effettuato_da_rel = relationship('EffettuanoClass', back_populates='viaggio_rel')

    #Biglietti associati al viaggio
    biglietti_rel = relationship('BigliettiClass', back_populates='viaggio_rel')

    #Voli che compongono il viaggio
    voli_rel = relationship('VoliClass', back_populates='viaggio_rel')