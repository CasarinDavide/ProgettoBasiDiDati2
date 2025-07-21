from System import Base
from typing import Literal    
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
CREATE TABLE dev.Biglietti (
                               id_biglietto VARCHAR(200) PRIMARY KEY,
                               categoria classe NOT NULL,
                               prezzo REAL NOT NULL,
                               posto VARCHAR(4) NOT NULL,
                               id_viaggio INTEGER REFERENCES dev.Viaggi(id_viaggio) ON DELETE CASCADE,
                               id_passeggero INTEGER REFERENCES dev.Passeggeri(id_passeggero) ON DELETE CASCADE
);
"""

class BigliettiClass(Base):
    __tablename__ = 'Biglietti'
    __table_args__ = { 'schema': 'dev' }

    id_biglietto: Mapped[str] = mapped_column(primary_key=True)
    categoria: Mapped[Literal['Economy', 'Business', 'FirstClass']] = mapped_column(nullable=False)
    prezzo: Mapped[float] = mapped_column(nullable=False)
    posto: Mapped[str] = mapped_column(nullable=False)
    
    # FK -> Viaggi
    id_viaggio = mapped_column(ForeignKey('dev.Viaggi.id_viaggio'), nullable=False)
    viaggio_rel = relationship('ViaggiClass', back_populates='biglietti_rel')
    
    # FK -> Passeggeri
    id_passeggero = mapped_column(ForeignKey('dev.Passeggeri.id_passeggero'), nullable=True)
    passeggero_rel = relationship('PasseggeriClass', back_populates='biglietti_rel')