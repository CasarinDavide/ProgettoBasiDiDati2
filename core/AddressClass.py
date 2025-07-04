from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from System import engine, Base

class AddressClass(Base):
    __tablename__ = 'address'

    # Attributi della tabella Address
    id_address: Mapped[str] = mapped_column(primary_key=True)
    civico: Mapped[str] = mapped_column(nullable=False)
    via: Mapped[str] = mapped_column(nullable=False)
    cod_postale: Mapped[int] = mapped_column(nullable=False)
    paese: Mapped[str] = mapped_column(nullable=False)

    # Lista di Users a cui è associato l'indirizzo
    users = relationship('UsersClass', back_populates="address")

    @classmethod
    def add(cls, _id_address, _civico, _via, _cod_postale, _paese):
        with session(engine) as session:
            record = cls(
                id_address = _id_address,
                civico = _civico,
                via = _via,
                cod_postale = _cod_postale,
                paese = _paese
            )
            session.add(record)

