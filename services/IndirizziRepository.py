from typing import Optional, List

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin

from core.IndirizziClass import IndirizziClass
from core.IndirizziClass import IndirizziClass
from services.BaseRepository import BaseRepository
from core.IndirizziClass import IndirizziClass
from services.BaseRepository import BaseRepository


class IndirizziRepository(BaseRepository[IndirizziClass]):

    def __init__(self):
        super().__init__(IndirizziClass)
        self.pk_field = "address_id"


    def add(self, civico: str, via: str, citta: str, cod_postale: str, paese: str) -> Optional[IndirizziClass]:
        """Create a new Compagnie record (custom wrapper)."""

        return super().add(
            civico= civico,
            via=via,
            citta=citta,
            cod_postale=cod_postale,
            paese=paese
        )

    def get_all(self) -> List["IndirizziClass"]:
        return super().get_all()

    def get_by_id(self, address_id: int) -> Optional["IndirizziClass"]:
        return super().get_by_id(address_id, pk_field=self.pk_field)

    def update(self,address_id,civico: str, via: str, citta: str, cod_postale: str, paese: str) -> bool:
        return self.update(address_id,
                           self.pk_field,
                           civico= civico,
                           via=via,
                           citta=citta,
                           cod_postale=cod_postale,
                           paese=paese)

    def delete(self, address_id: int) -> bool:
        return self.delete(address_id, self.pk_field)

    def get_datatable(self, draw: int, start: int, length: int, search_value: str):
        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=[""])

    def create_if_not_exists(self,civico: str, via: str, citta: str, cod_postale: str, paese: str):
        row = super().search_single_by_columns(civico = civico,
                                               via = via,
                                               citta = citta,
                                               cod_postale = cod_postale,
                                               paese = paese)
        if row is not None:
            return row.address_id
        else:
            return self.add(civico = civico,
                     via = via,
                     citta = citta,
                     cod_postale = cod_postale,
                     paese = paese).address_id
