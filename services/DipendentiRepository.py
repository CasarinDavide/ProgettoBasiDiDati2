from __future__ import annotations

from typing import Optional, List

from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin

from core.CompagnieClass import CompagnieClass
from services.BaseRepository import BaseRepository, model_to_dict
from core.DipendentiClass import DipendentiClass
from services.BaseRepository import BaseRepository

class DipendentiRepository(BaseRepository[DipendentiClass]):

    def __init__(self):
        super().__init__(DipendentiClass)
        self.pk_field = "id_dipendente"

    def add(self, email: str, password: str, tel: str, nome: str,
            cognome: str, ruolo: str,id_compagnia:str) -> Response:
        """Create a new Dipendenti record (custom wrapper)."""

        rec = super().add(
            email=email,
            password=generate_password_hash(password),
            tel=tel,
            nome=nome,
            cognome=cognome,
            ruolo=ruolo,
            id_compagnia = id_compagnia
        )

        if rec is None:
            return jsonify({"success":False})

        return jsonify({"success":True})

    def get_all(self) -> Response:
        """Fetch all Dipendenti records."""
        return jsonify([model_to_dict(dipendente) for dipendente in super().get_all()])

    def get_by_id(self, dipendente_id: str) -> Response:
        """Fetch a single Dipendenti by ID."""

        return jsonify(model_to_dict(super().get_by_id(int(dipendente_id), pk_field=self.pk_field,joins=[]),backrefs = True))


    def update(self, dipendente_id: int, email: str, tel: str, nome: str,
               cognome: str, ruolo: str,id_compagnia:str) -> Response:
        """
        Update a Dipendenti.
        kwargs can include email, password, tel, nome, address_id.
        """
        res = super().update(dipendente_id,
                            self.pk_field,
                            email=email,
                            tel=tel,
                            nome=nome,
                            cognome=cognome,
                            id_compagnia=int(id_compagnia))
        return jsonify({"success":res})

    def delete(self, dipendente_id: int) -> Response:
        """Delete a Dipendenti by ID."""
        res = super().delete(dipendente_id, self.pk_field)
        return jsonify({"success":res})

    def get_datatable(self, draw: int, start: int, length: int, search_value: str,id_compagnia = str):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["email","nome","cognome","tel"],
                                     id_compagnia = int(id_compagnia),
                                     joins=[DipendentiClass.compagnia_rel])
