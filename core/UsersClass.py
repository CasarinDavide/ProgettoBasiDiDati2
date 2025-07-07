from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash
from System import engine, Base
from flask_login import UserMixin

#UserMixin è la classe da ereditare per Flask-Login
class UsersClass(UserMixin, Base):
    __tablename__ = 'users'

    # Attributi della tabella Users
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    #ForeignKey -> Address
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'), nullable=False)

    # Address associato all'utente
    # la stringa in 'back_populates' corrisponde al nome dell'attributo presente nell'altra classe (non al nome della classe)   
    address_rel = relationship('AddressesClass', back_populates='users_rel')

    #alternativa: relationship(Address, backref='users')
    #questo metodo permette di togliere l'attributo users da Address perché lo crea da solo, ma mi pareva più chiaro usare 'back_populates' normale

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'tel': self.tel,
            'address': self.address
        }

    @classmethod
    def add(cls, email, password, tel, address):
        with Session(engine()) as session:
            record = cls(
                email = email,
                password = password,
                tel = tel,
                address_id = address
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
    def get_by_email(cls, _email):
        with Session(engine()) as session:
            return session.query(cls).filter_by(email=_email).first()
    
    @classmethod
    def get_by_id(cls, user_id):
        with Session(engine()) as session:
            return session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def validate_password(cls, email, password):
        user = cls.get_by_email(email)
        if user and check_password_hash(user.password, password):
            return True  # Password is correct
        return False  # Password is incorrect
    
    def get_id(self):
        return str(self.id)
