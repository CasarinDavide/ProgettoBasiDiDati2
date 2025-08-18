from __future__ import annotations

from typing import Optional, List

from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash, generate_password_hash

from core.AereiClass import AereiClass
from core.AdminClass import AdminClass
from services.BaseRepository import BaseRepository, model_to_dict
from core.AdminClass import AdminClass
from services.BaseRepository import BaseRepository

class AdminRepository(BaseRepository[AdminClass]):

    def __init__(self):
        super().__init__(AdminClass)
        self.pk_field = "id"

    def get_by_id_json(self, id: str) -> Response:
        """Fetch a single compagnie by ID."""

        return jsonify(model_to_dict(super().get_by_id(int(id), pk_field=self.pk_field,joins=[]),backrefs = True))
    
    def get_by_id(self, id: str,**kwargs) -> AdminClass | None:
        return super().get_by_id(int(id), pk_field=self.pk_field)

    def validate_password(self, email: str, password: str) -> bool:
        user = super().search_single_by_columns(email=email)
        
        return user and check_password_hash(user.password, password)

    def get_by_email(self, email: str) -> AdminClass | None:
        return super().search_single_by_columns(email=email)

    
