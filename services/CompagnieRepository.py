from __future__ import annotations

from typing import Optional, List

from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from core.CompagnieClass import CompagnieClass
from services.BaseRepository import BaseRepository, model_to_dict
from core.CompagnieClass import CompagnieClass
from services.BaseRepository import BaseRepository

class CompagnieRepository(BaseRepository[CompagnieClass]):

    def __init__(self):
        super().__init__(CompagnieClass)
        self.pk_field = "id_compagnia"

    def add(self, email: str, password: str, tel: str, nome: str,
                    civico: str, via: str, citta: str, cod_postale: str, paese: str) -> Response:
        """Create a new Compagnie record (custom wrapper)."""


        rec = super().add(
            email=email,
            password=generate_password_hash(password),
            tel=tel,
            nome=nome,
            civico=civico,
            via=via,
            cod_postale=cod_postale,
            citta=citta,
            paese=paese
        )

        if rec is None:
            return jsonify({"success":False})

        return jsonify({"success":True})

    def get_all(self) -> Response:
        """Fetch all compagnie records."""
        return jsonify([model_to_dict(compagnia) for compagnia in super().get_all()])

    def get_by_id_json(self, compagnie_id: str) -> Response:
        """Fetch a single compagnie by ID."""

        return jsonify(model_to_dict(super().get_by_id(int(compagnie_id), pk_field=self.pk_field,joins=[]),backrefs = True))
    
    def get_by_id(self, id_compagnia: str) -> CompagnieClass | None:
        return super().get_by_id(int(id_compagnia), pk_field=self.pk_field)

    def update(self, compagnie_id: int, email: str, tel: str, nome: str, civico: str, via: str, citta: str, cod_postale: str, paese: str) -> Response:
        """
        Update a compagnie.
        kwargs can include email, password, tel, nome, address_id.
        """
        res = super().update(compagnie_id,
                            self.pk_field,
                            email=email,
                            tel=tel,
                            nome=nome,
                            civico=civico,
                            via=via,
                            cod_postale=cod_postale,
                            citta=citta,
                            paese=paese)
        return jsonify({"success":res})

    def delete(self, compagnie_id: int) -> Response:
        """Delete a compagnie by ID."""
        res = super().delete(compagnie_id, self.pk_field)
        return jsonify({"success":res})

    def get_datatable(self, draw: int, start: int, length: int, search_value: str):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["email","nome","tel"])
    
    def validate_password(self, email: str, password: str) -> bool:
        user = super().search_single_by_columns(email=email)
        
        return user and check_password_hash(user.password, password)

    def get_by_email(self, email: str) -> CompagnieClass | None:
        return super().search_single_by_columns(email=email)



