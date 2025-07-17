from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
-- Aereoporti
CREATE TABLE dev.Aereoporti (
                                id_aereoporto SERIAL PRIMARY KEY,
                                nome VARCHAR(200) NOT NULL,
                                via VARCHAR(200) NOT NULL,
                                civico VARCHAR(200) NOT NULL,
                                cod_postale INTEGER NOT NULL,
                                citta VARCHAR(200) NOT NULL,
                                paese VARCHAR(200) NOT NULL
);
"""
class AereoportiClass(Base):
    __tablename__ = 'Aereoporti'
    __table_args__ = { 'schema': 'dev' }

    id_aereoporto: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    
    via: Mapped[str] = mapped_column(nullable=False)
    civico: Mapped[str] = mapped_column(nullable=False)
    cod_postale: Mapped[int] = mapped_column(nullable=False)
    citta: Mapped[str] = mapped_column(nullable=False)
    paese: Mapped[str] = mapped_column(nullable=False)

    viaggi_partenza_rel = relationship('ViaggiClass', foreign_keys='ViaggiClass.id_aereoporto_partenza', back_populates='partenza_rel')

    viaggi_arrivo_rel = relationship('ViaggiClass', foreign_keys='ViaggiClass.id_aereoporto_arrivo', back_populates='arrivo_rel')