from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey
from datetime import datetime
from System import engine, Base
from flask_login import UserMixin
"""
CREATE TABLE dev.Passeggeri (
                                id_passeggero SERIAL PRIMARY KEY,
                                email VARCHAR(200) UNIQUE NOT NULL,
                                password VARCHAR(255) NOT NULL,
                                nome VARCHAR(200) NOT NULL,
                                cognome VARCHAR(200) NOT NULL,
                                tel VARCHAR(20) NOT NULL,
                                nascita DATE NOT NULL,
                                saldo REAL NOT NULL,
                                via VARCHAR(200) NOT NULL,
                                civico VARCHAR(200) NOT NULL,
                                cod_postale INTEGER NOT NULL,
                                citta VARCHAR(200) NOT NULL,
                                paese VARCHAR(200) NOT NULL
);
"""
#UserMixin è la classe da ereditare per Flask-Login
class PasseggeriClass(UserMixin, Base):
    __tablename__ = 'Passeggeri'
    __table_args__ = { 'schema': 'dev' }

    # Attributi della tabella Users
    id_passeggero: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    nascita: Mapped[datetime] = mapped_column(nullable=False)
    saldo: Mapped[float] = mapped_column(nullable=False)
    
    via: Mapped[str] = mapped_column(nullable=False)
    civico: Mapped[str] = mapped_column(nullable=False)
    cod_postale: Mapped[int] = mapped_column(nullable=False)
    citta: Mapped[str] = mapped_column(nullable=False)
    paese: Mapped[str] = mapped_column(nullable=False)

    # Biglietti posseduti dal passeggero
    # la stringa in 'back_populates' corrisponde al nome dell'attributo presente nell'altra classe (non al nome della classe)   

    #alternativa: relationship(NomeClass, backref='passeggeri')
    #questo metodo permette di togliere l'attributo passeggeri da Biglietti perché lo crea da solo, ma mi pareva più chiaro usare 'back_populates' normale
    biglietti_rel = relationship('BigliettiClass', back_populates='passeggero_rel')
    
    def get_id(self):
        return str(self.id_passeggero)
