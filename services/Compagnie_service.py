from typing import Optional, List

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin

from core.CompagnieClass import CompagnieClass


def add_compagnie(email: str, password: str, tel: str, nome: str, address_id: int) -> Optional["CompagnieClass"]:
    """Create a new Compagnie record."""
    print("QUI")
    # MUST ASSUME RIGHT INPUT VALUE

    with Session(engine()) as session:
        record = CompagnieClass(
            email=email,
            password=password,
            tel=tel,
            nome=nome,
            address_id=0
        )
        session.add(record)
        session.commit()
        print("PROVA")
        session.refresh(record)
        return True



def get_all_compagnie() -> List["CompagnieClass"]:
    """Fetch all compagnie records."""
    res = None
    with Session(engine()) as session:
        res = session.query(CompagnieClass).all()
    return res


def get_compagnie_by_id(compagnie_id: int) -> Optional["CompagnieClass"]:
    """Fetch a single compagnie by ID."""
    row = None
    with Session(engine()) as session:
        row = session.query(CompagnieClass).filter_by(id_compagnie=compagnie_id).first()
    return row




def update_compagnie(compagnie_id: int,email: str, password: str, tel: str, nome: str, address_id: int) -> Optional["CompagnieClass"]:
    """
    Update a compagnie.
    kwargs can include email, password, tel, nome, address_id.
    """
    comp = get_compagnie_by_id(compagnie_id)
    if not comp:
        return False

    comp.email = email
    comp.tel = tel
    comp.nome = nome
    comp.address_id = address_id

    with Session(engine()) as session:
        session.commit()
        return True

def delete_compagnie(compagnie_id: int) -> bool:
    """Delete a compagnie by ID."""
    comp = get_compagnie_by_id(compagnie_id)
    if not comp:
        return False

    with Session(engine()) as session:
        session.delete(comp)
        session.commit()
        return True

def get_compagnie_datatable(draw:int,start:int,length:int,search_value:str):

    data = []

    with Session(engine()) as session:
        query = session.query(CompagnieClass)
        records_total = query.count()
        if search_value:
            query = query.filter(
                CompagnieClass.nome.ilike(f"%{search_value}%") |
                CompagnieClass.email.ilike(f"%{search_value}%") |
                CompagnieClass.tel.ilike(f"%{search_value}%")
            )
        records_filtered = query.count()
        compagnies = query.offset(start).limit(length).all()
        data = [
            [c.id_compagnie, c.nome, c.email, c.tel]
            for c in compagnies
        ]


    return jsonify({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })