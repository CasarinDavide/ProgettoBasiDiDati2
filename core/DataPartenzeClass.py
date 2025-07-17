from System import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

"""
CREATE TABLE dev.DataPartenze (
                                  id_data_partenza SERIAL PRIMARY KEY,
                                  id_viaggio INTEGER REFERENCES dev.Viaggi(id_viaggio) ON DELETE CASCADE,
                                  data DATE NOT NULL
);
"""
class DataPartenzeClass(Base):
    __tablename__ = 'DataPartenze'
    __table_args__ = { 'schema': 'dev' }


    id_data_partenza: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime] = mapped_column(nullable=False)
    
    # FK -> Viaggi
    id_viaggio: Mapped[int] = mapped_column(ForeignKey('dev.Viaggi.id_viaggio'), nullable=False)

    viaggio_rel = relationship('ViaggiClass', back_populates='data_partenze_rel')



