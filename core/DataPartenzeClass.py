from System import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class DataPartenzeClass(Base):
    __tablename__ = 'DataPartenze'
    __table_args__ = { 'schema': 'dev' }
    

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime] = mapped_column(nullable=False)
    
    # FK -> Viaggi
    id_viaggio: Mapped[int] = mapped_column(ForeignKey('dev.Viaggi.id'), nullable=False)

    viaggio_rel = relationship('ViaggiClass', back_populates='data_partenze_rel')