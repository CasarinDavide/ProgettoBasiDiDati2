from System import Base
from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class BigliettiClass(Base):
    __tablename__ = 'Biglietti'
    __table_args__ = { 'schema': 'dev' }

    id: Mapped[str] = mapped_column(primary_key=True)
    categoria: Mapped[Enum] = mapped_column(nullable=False)
    prezzo: Mapped[float] = mapped_column(nullable=False)
    posto: Mapped[str] = mapped_column(nullable=False)
    
    # FK -> Viaggi
    id_viaggio = mapped_column(ForeignKey('dev.Viaggi.id'), nullable=False)
    viaggio_rel = relationship('ViaggiClass', back_populates='biglietti_rel')
    
    # FK -> Passeggeri
    id_passeggero = mapped_column(ForeignKey('dev.Passeggeri.id'), nullable=True)
    passeggero_rel = relationship('PasseggeriClass', back_populates='biglietti_rel')