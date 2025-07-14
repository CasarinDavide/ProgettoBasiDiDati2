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

    id_voli: Mapped[int] = mapped_column(primary_key=True)
    comandante: Mapped[str] = mapped_column(nullable=False)
    ritardo: Mapped[int] = mapped_column(nullable=False)

    # FK -> Viaggi
    id_viaggio: Mapped[int] = mapped_column(ForeignKey('dev.Viaggi.id_viaggio'), primary_key=True)
    viaggio_rel = relationship('ViaggiClass', back_populates='voli_rel')
    
    # FK -> Aerei
    id_aereo: Mapped[int] = mapped_column(ForeignKey('dev.Aerei.id_aerei'), primary_key=True)
    aereo_rel = relationship('AereiClass', back_populates='voli_rel')   