from __future__ import annotations

from typing import Optional, List

from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin

from core.AereiClass import AereiClass
from core.AereiClass import AereiClass
from services.BaseRepository import BaseRepository, model_to_dict
from core.AereiClass import AereiClass
from services.BaseRepository import BaseRepository


class AereiRepository(BaseRepository[AereiClass]):

    def __init__(self):
        super().__init__(AereiClass)
        self.pk_field = "id_aereo"

    def add(self, capacita: str, modello: str, consumoMedio: str, dimensione: str,id_compagnia:Optional[None] | Optional[str],
                        seat_row_number_first:int = 1,
                        seat_column_number_first:int = 1,
                        seat_row_number_business:int = 1,
                        seat_column_number_business:int = 1,
                        seat_row_number_economy:int = 1,
                        seat_column_number_economy:int = 1) -> Response:

        """Create a new Compagnie record (custom wrapper)."""

        
        rec = super().add(
            capacita = capacita,
            modello = modello,
            consumoMedio = consumoMedio,
            dimensione = dimensione,
            id_compagnia = id_compagnia,
            seat_row_number_first = seat_row_number_first,
            seat_column_number_first = seat_column_number_first,
            seat_row_number_business= seat_row_number_business,
            seat_column_number_business= seat_column_number_business,
            seat_row_number_economy= seat_row_number_economy,
            seat_column_number_economy=seat_column_number_economy
        )

        if rec is None:
            jsonify({"success":False})

        return jsonify({"success":True})

    def get_all(self,**kwargs) -> List["AereiClass"]:
        """Fetch all compagnie records."""
        return jsonify([model_to_dict(aereo,backrefs=True) for aereo in super().get_all(joins=[AereiClass.compagnia_rel],**kwargs)])


    def get_by_id(self, id_aereo: str) -> Response:
        """Fetch a single compagnie by ID."""

        return jsonify(model_to_dict(super().get_by_id(int(id_aereo), pk_field=self.pk_field, joins=[AereiClass.compagnia_rel]), backrefs=True))


    def update(self, id_aereo: int, capacita: str, modello: str, consumoMedio: str, dimensione: str,id_compagnia:Optional[None] | Optional[str],
               seat_row_number_first:int = 1,
               seat_column_number_first:int = 1,
               seat_row_number_business:int = 1,
               seat_column_number_business:int = 1,
               seat_row_number_economy:int = 1,
               seat_column_number_economy:int = 1) -> Response:
        """
        Update a compagnie.
        kwargs can include email, password, tel, nome, address_id.
        """
        res = super().update(id_aereo,
                           self.pk_field,
                           capacita=capacita,
                             modello=modello,
                             consumoMedio=consumoMedio,
                             dimensione=dimensione,
                             id_compagnia=id_compagnia,
                             seat_row_number_first = seat_row_number_first,
                             seat_column_number_first = seat_column_number_first,
                             seat_row_number_business= seat_row_number_business,
                             seat_column_number_business= seat_column_number_business,
                             seat_row_number_economy= seat_row_number_economy,
                             seat_column_number_economy=seat_column_number_economy)
        return jsonify({"success":res})

    def delete(self, id_aereo: int) -> Response:
        """Delete a compagnie by ID."""
        res = super().delete(id_aereo, self.pk_field)
        return jsonify({"success":res})

    def get_datatable(self, draw: int, start: int, length: int, search_value: str,**kwargs):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["email","nome","tel"],joins=[AereiClass.compagnia_rel],id_compagnia = kwargs.get('id_compagnia',''))
