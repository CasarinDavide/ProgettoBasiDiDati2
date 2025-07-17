from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
-- Aereoporti
CREATE TABLE dev.Aereoporti (
                                id_aereoporto SERIAL PRIMARY KEY,
                                nome VARCHAR(200) NOT NULL,
                                address_id INTEGER REFERENCES dev.Indirizzi(address_id) ON DELETE SET NULL
);
"""
class AereoportiClass(Base):
    __tablename__ = 'Aereoporti'
    __table_args__ = { 'schema': 'dev' }

    id_aereoporto: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    # FK -> Indirizzi
    address_id: Mapped[int] = mapped_column(ForeignKey('dev.Indirizzi.address_id'), nullable=False)
    address_rel = relationship('IndirizziClass', back_populates='aereoporto_rel')

    viaggi_partenza_rel = relationship('ViaggiClass', foreign_keys='ViaggiClass.partenza', back_populates='partenza_rel')
    
    viaggi_arrivo_rel = relationship('ViaggiClass', foreign_keys='ViaggiClass.arrivo', back_populates='arrivo_rel')