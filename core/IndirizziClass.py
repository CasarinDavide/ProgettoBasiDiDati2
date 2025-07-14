from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from System import engine, Base

"""
CREATE TABLE dev.Indirizzi (
    address_id SERIAL PRIMARY KEY,
civico VARCHAR(200) NOT NULL,
via VARCHAR(200) NOT NULL,
citta VARCHAR(100) NOT NULL,
cod_postale INTEGER NOT NULL,
paese VARCHAR(100) NOT NULL
);
"""

class IndirizziClass(Base):
    __tablename__ = 'Indirizzi'
    __table_args__ = { 'schema': 'dev' }


    # Attributi della tabella Address
    address_id: Mapped[int] = mapped_column(primary_key=True)
    civico: Mapped[str] = mapped_column(nullable=False)
    via: Mapped[str] = mapped_column(nullable=False)
    citta: Mapped[str] = mapped_column(nullable=False)
    cod_postale: Mapped[int] = mapped_column(nullable=False)
    paese: Mapped[str] = mapped_column(nullable=False)

    # Passeggeri a cui è associato l'indirizzo
    passeggeri_rel = relationship('PasseggeriClass', back_populates='address_rel')
    # Compagnie a cui è associato l'indirizzo
    compagnia_rel = relationship('CompagnieClass', back_populates='address_rel')
    # Aereoporto a cui è associato l'indirizzo
    aereoporto_rel = relationship('AereoportiClass', back_populates='address_rel')
    
    @classmethod
    def add(cls, civico, via, citta, cod_postale, paese):
        with Session(engine()) as session:
            record = cls(
                civico = civico,
                via = via,
                citta = citta,
                cod_postale = cod_postale,
                paese = paese
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    @classmethod
    def get_address(cls, civico, via, citta, cod_postale, paese):
        with Session(engine()) as session:
            return session.query(cls).filter(
                cls.civico == civico,
                cls.via == via,
                cls.citta == citta,
                cls.cod_postale == cod_postale,
                cls.paese == paese
            ).first()
