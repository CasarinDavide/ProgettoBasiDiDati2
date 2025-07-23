from __future__ import annotations

from typing import Optional, List

from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin

from core.CompagnieClass import CompagnieClass
from services.BaseRepository import BaseRepository, model_to_dict
from core.AereoportiClass import AereoportiClass
from services.BaseRepository import BaseRepository

class AereoportiRepository(BaseRepository[AereoportiClass]):

    def __init__(self):
        super().__init__(AereoportiClass)
        self.pk_field = "id_aereoporto"

    def add(self,id_aereoporto:str, nome: str, civico: str, via: str, cod_postale: str,citta: str,paese: str) -> Response:
        """Create a new Compagnie record (custom wrapper)."""

        # check uniqueness id_aereoporto
        res = super().get_by_id(id_aereoporto, pk_field=self.pk_field)
        if res is None:
            rec = super().add(
                id_aereoporto = id_aereoporto,
                nome = nome,
                civico = civico,
                via = via,
                cod_postale = cod_postale,
                citta = citta,
                paese = paese
            )

            if rec is None:
                return jsonify({"success":False})
        else:
            return  jsonify({"success":True,"Message":"Record già presente"})

        return jsonify({"success":True})

    def get_all(self) -> Response:
        """Fetch all Aereoporti records."""
        return jsonify([model_to_dict(aereoporti) for aereoporti in super().get_all()])

    def get_by_id(self, id_aereoporto: str) -> Response:
        """Fetch a single Aereoporti by ID."""

        return jsonify(model_to_dict(super().get_by_id(id_aereoporto, pk_field=self.pk_field,joins=[]),backrefs = True))


    def update(self, id_aereoporto: str, nome: str, civico: str, via: str, cod_postale: str,citta: str,paese: str) -> Response:
        """
        Update a Aereoporti.
        kwargs can include email, password, tel, nome, address_id.
        """
        res = super().update(id_aereoporto,
                            self.pk_field,
                            nome = nome,
                            civico = civico,
                            via = via,
                            cod_postale = cod_postale,
                            citta = citta,
                            paese = paese)
        return jsonify({"success":res})

    def delete(self, id_aereoporto: str) -> Response:
        """Delete a Aereoporti by ID."""
        res = super().delete(id_aereoporto, self.pk_field)
        return jsonify({"success":res})

    def get_datatable(self, draw: int   , start: int, length: int, search_value: str):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["nome","citta"])
