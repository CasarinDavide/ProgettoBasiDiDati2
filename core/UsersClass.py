from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from hashlib import sha256
from System import engine, Base

class UsersClass(Base):
    __tablename__ = 'users'

    # Attributi della tabella Users
    id_user: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(unique=True, nullable=False)
    #ForeignKey -> Address
    addr: Mapped[int] = mapped_column(ForeignKey('address.id_address'), nullable=False)

    # Address associato all'utente
    # la stringa in 'back_populates' corrisponde al nome dell'attributo presente nell'altra classe (non al nome della classe)   
    address = relationship('AddressClass', back_populates='users')

    #alternativa: relationship(Address, backref='users')
    #questo metodo permette di togliere l'attributo users da Address perché lo crea da solo, ma mi pareva più chiaro usare 'back_populates' normale

    def to_dict(self):
        return {
            'id_user': self.id_utente,
            'email': self.email,
            'password': self.password,
            'tel': self.tel,
            'address': self.addr
        }

    @classmethod
    def add(cls, _id_user, _email, _password, _tel, _address):
        with session(engine) as session:
            record = cls(
                id_user = _id_user,
                email = _email,
                password = sha256(_password).hexdigest(),
                tel = _tel,
                addr = _address
            )
            session.add(record)

    @classmethod
    def get_all(cls):
        with session(engine) as session:
            records = session.query(cls).all()
            return [record.to_dict() for record in records]

    @classmethod
    def get_by_email(cls, _email):
        with session(engine) as session:
            return session.query(cls).filter_by(email=_email).first()

    @classmethod
    def get(cls, _id_utente):
        with session(engine) as session:
            return session.query(cls).filter_by(id_utente=_id_utente).first()


    @classmethod
    def validate_password(cls, email, password):
        user = cls.get_by_email(email)
        if user and user.password == sha256(password).hexdigest():
            return True  # Password is correct
        return False  # Password is incorrect
