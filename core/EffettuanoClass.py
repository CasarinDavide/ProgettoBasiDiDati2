from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class EffettuanoClass(Base):
    __tablename__ = 'Effettuano'
    __table_args__ = { 'schema': 'dev' }
    
    # FK -> Compagnie
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id'), primary_key=True)
    compagnia_rel = relationship('CompagnieClass', back_populates='effettuano_rel')
    
    # FK -> Viaggi
    id_viaggio: Mapped[int] = mapped_column(ForeignKey('dev.Viaggi.id'), primary_key=True)
    viaggio_rel = relationship('ViaggiClass', back_populates='effettuato_da_rel')