from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
"""
CREATE TABLE dev.Effettuano (
                                id_compagnia INTEGER REFERENCES dev.Compagnie(id_compagnie) ON DELETE CASCADE,
                                id_viaggio INTEGER REFERENCES dev.Viaggi(id_viaggio) ON DELETE CASCADE,
                                PRIMARY KEY(id_compagnia, id_viaggio)
);
"""
class EffettuanoClass(Base):
    __tablename__ = 'Effettuano'
    __table_args__ = { 'schema': 'dev' }
    
    # FK -> Compagnie
    id_compagnia: Mapped[int] = mapped_column(ForeignKey('dev.Compagnie.id_compagnia'), primary_key=True)
    compagnia_rel = relationship('CompagnieClass', back_populates='effettuano_rel')
    
    # FK -> Viaggi
    id_viaggio: Mapped[int] = mapped_column(ForeignKey('dev.Viaggi.id_viaggio'), primary_key=True)
    viaggio_rel = relationship('ViaggiClass', back_populates='effettuato_da_rel')