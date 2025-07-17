from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey
from datetime import datetime
from werkzeug.security import check_password_hash
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

    def to_dict(self):
        return {
            'id': self.id_passeggero,
            'email': self.email,
            'password': self.password,
            'nome': self.nome,
            'cognome': self.cognome,
            'tel': self.tel,
            'nascita': self.nascita,
            'saldo': self.saldo,
            'via': self.via,
            'civico': self.civico, 
            'cod_postale': self.cod_postale, 
            'citta': self.citta, 
            'paese': self.paese
        }

    @classmethod
    def add(cls, email, password, nome, cognome, tel, nascita, saldo, via, civico, cod_postale, citta, paese):
        with Session(engine()) as session:
            record = cls(
                email = email,
                password = password,
                nome = nome,
                cognome = cognome,
                tel = tel,
                nascita = nascita,
                saldo = saldo,
                via = via,
                civico = civico, 
                cod_postale = cod_postale, 
                citta = citta, 
                paese = paese
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    @classmethod
    def get_all(cls):
        with Session(engine()) as session:
            records = session.query(cls).all()
            return [record.to_dict() for record in records]

    @classmethod
    def get_by_email(cls, email):
        with Session(engine()) as session:
            return session.query(cls).filter_by(email=email).first()
    
    @classmethod
    def get_by_id(cls, user_id):
        with Session(engine()) as session:
            return session.query(cls).filter_by(id_passeggero=user_id).first()

    @classmethod
    def validate_password(cls, email, password):
        user = cls.get_by_email(email)
        if user and check_password_hash(user.password, password):
            return True  # Password is correct
        return False  # Password is incorrect
    
    def get_id(self):
        return str(self.id_passeggero)
