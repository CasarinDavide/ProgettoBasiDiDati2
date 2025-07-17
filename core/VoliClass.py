from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
CREATE TABLE dev.Voli (
                          id_voli SERIAL PRIMARY KEY,
                          comandante VARCHAR(200) NOT NULL,
                          ritardo INTEGER NOT NULL,
                          id_viaggio INTEGER REFERENCES dev.Viaggi(id_viaggio) ON DELETE CASCADE,
                          id_aereo INTEGER REFERENCES dev.Aerei(id_aerei) ON DELETE CASCADE
);
"""
class VoliClass(Base):
    __tablename__ = 'Voli'
    __table_args__ = { 'schema': 'dev' }

    id_volo: Mapped[int] = mapped_column(primary_key=True)
    comandante: Mapped[str] = mapped_column(nullable=False)
    ritardo: Mapped[int] = mapped_column(nullable=False)

    # FK -> Viaggi
    id_viaggio: Mapped[int] = mapped_column(ForeignKey('dev.Viaggi.id_viaggio'))
    viaggio_rel = relationship('ViaggiClass', back_populates='voli_rel')
    
    # FK -> Aerei
    id_aereo: Mapped[int] = mapped_column(ForeignKey('dev.Aerei.id_aereo'))
    aereo_rel = relationship('AereiClass', back_populates='voli_rel')

    # FK -> Aereoporti
    id_aereoporto_partenza: Mapped[int] = mapped_column(ForeignKey('dev.Aereoporti.id_aereoporto'), nullable=False)
    aereoporto_partenza_rel = relationship('AereoportiClass', foreign_keys=[id_aereoporto_partenza], back_populates='voli_partenza_rel')

    # FK -> Aereoporti
    id_aereoporto_arrivo: Mapped[int] = mapped_column(ForeignKey('dev.Aereoporti.id_aereoporto'), nullable=False)
    aereoporto_arrivo_rel = relationship('AereoportiClass', foreign_keys=[id_aereoporto_arrivo], back_populates='voli_arrivo_rel')