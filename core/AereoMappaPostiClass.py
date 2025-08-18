from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AereoMappaPostiClass(Base):
    __tablename__ = 'AereoMappaPosti'
    __table_args__ = { 'schema': 'dev' }

    id_posto: Mapped[int] = mapped_column(primary_key=True)
    id_aereo: Mapped[int] = mapped_column(nullable=False)
    seat_label: Mapped[str] = mapped_column(nullable=False)
    seat_column: Mapped[float] = mapped_column(nullable=False)
    seat_row: Mapped[str] = mapped_column(nullable=False)
    seat_class: Mapped[int] = mapped_column(nullable=False)
