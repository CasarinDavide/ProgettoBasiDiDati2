from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from System import engine, Base

class AddressClass(Base):
    __tablename__ = 'address'

    # Attributi della tabella Address
    id: Mapped[int] = mapped_column(primary_key=True)
    civico: Mapped[str] = mapped_column(nullable=False)
    via: Mapped[str] = mapped_column(nullable=False)
    citta: Mapped[str] = mapped_column(nullable=False)
    cod_postale: Mapped[int] = mapped_column(nullable=False)
    paese: Mapped[str] = mapped_column(nullable=False)

    # Lista di Users a cui è associato l'indirizzo
    users = relationship('UsersClass', back_populates="address")

    @classmethod
    def add(cls, _civico, _via, _citta, _cod_postale, _paese):
        with Session(engine()) as session:
            record = cls(
                civico = _civico,
                via = _via,
                citta = _citta,
                cod_postale = _cod_postale,
                paese = _paese
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    @classmethod
    def get_address(cls, _civico, _via, _citta, _cod_postale, _paese):
        with Session(engine()) as session:
            return session.query(cls).filter(
                cls.civico == _civico,
                cls.via == _via,
                cls.citta == _citta,
                cls.cod_postale == _cod_postale,
                cls.paese == _paese
            ).first()
