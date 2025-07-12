from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ViaggiClass(Base):
    __tablename__ = 'Viaggi'
    __table_args__ = { 'schema': 'dev' }    

    id: Mapped[int] = mapped_column(primary_key=True)
    sosta: Mapped[int] = mapped_column(nullable=False)
    durata: Mapped[int] = mapped_column(nullable=False)
    sconto: Mapped[float] = mapped_column(nullable=False)
    
    # FK -> Aereoporto Partenza
    partenza: Mapped[int] = mapped_column(ForeignKey('dev.Aereoporti.id'), nullable=False)
    partenza_rel = relationship('AereoportiClass', foreign_keys=[partenza],back_populates='viaggi_partenza_rel')
    
    # FK -> Aereoporto Arrivo
    arrivo: Mapped[int] = mapped_column(ForeignKey('dev.Aereoporti.id'), nullable=False)
    arrivo_rel = relationship('AereoportiClass', foreign_keys=[arrivo],back_populates='viaggi_arrivo_rel')

    #Date di partenza associate al viaggio
    data_partenze_rel = relationship('DataPartenzeClass', back_populates='viaggio_rel')

    #Compagnie Aree che effettuano questo viaggio
    effettuato_da_rel = relationship('EffettuanoClass', back_populates='viaggio_rel')

    #Biglietti associati al viaggio
    biglietti_rel = relationship('BigliettiClass', back_populates='viaggio_rel')

    #Voli che compongono il viaggio
    voli_rel = relationship('VoliClass', back_populates='viaggio_rel')