from typing import Optional, List

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from System import engine, Base

from System import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from flask_login import UserMixin

from core.CompagnieClass import CompagnieClass
from services.BaseRepository import BaseRepository
from core.CompagnieClass import CompagnieClass
from services.BaseRepository import BaseRepository


class CompagnieRepository(BaseRepository[CompagnieClass]):

    def __init__(self):
        super().__init__(CompagnieClass)
        self.pk_field = "id_compagnie"

    def add(self, email: str, password: str, tel: str, nome: str, address_id: int) -> Optional[CompagnieClass]:
        """Create a new Compagnie record (custom wrapper)."""
        return super().add(
            email=email,
            password=password,
            tel=tel,
            nome=nome,
            address_id=address_id
        )

    def get_all(self) -> List["CompagnieClass"]:
        """Fetch all compagnie records."""
        return super().get_all()

    def get_by_id(self, compagnie_id: int) -> Optional["CompagnieClass"]:
        """Fetch a single compagnie by ID."""
        return super().get_by_id(compagnie_id, pk_field=self.pk_field)

    def update(self, compagnie_id: int, email: str, password: str, tel: str, nome: str,
                         address_id: int) -> bool:
        """
        Update a compagnie.
        kwargs can include email, password, tel, nome, address_id.
        """
        return self.update(compagnie_id,
                           self.pk_field,
                           email=email,
                           password=password,
                           tel=tel,
                           nome=nome,
                           address_id=address_id)

    def delete(self, compagnie_id: int) -> bool:
        """Delete a compagnie by ID."""
        return self.delete(compagnie_id, self.pk_field)

    def get_datatable(self, draw: int, start: int, length: int, search_value: str):
        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=[""])
