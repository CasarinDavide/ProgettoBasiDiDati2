from core.PasseggeriClass import PasseggeriClass
from services.BaseRepository import BaseRepository, model_to_dict
from datetime import datetime

from flask import jsonify, Response
from werkzeug.security import check_password_hash



class PasseggeriRepository(BaseRepository[PasseggeriClass]):
    
    def __init__(self):
        super().__init__(PasseggeriClass)
        self.pk_field = "id_passeggero"
        

    def add(self, email: str, password:str , nome: str, cognome: str, tel: str, nascita: datetime, saldo: float, via: str, civico: str, cod_postale: int, citta: str, paese: str) -> Response:
        
        record = super.add(
            email = email,
            password = password,
            nome = nome,
            cognome = cognome,
            tel = tel,
            nascita = nascita,
            saldo = saldo,
            via = via,
            civico = civico, 
            cod_postale = cod_postale, 
            citta = citta, 
            paese = paese
        )
        
        if record is None:
            return jsonify({ "success": False })

    def get_all(self) -> Response:
        return jsonify( [model_to_dict(passeggero) for passeggero in super.get_all()] )

    def get_by_id(self, id: str):
        return super().search_single_by_columns(id_passeggero=id)
    
    def get_by_email(self, email: str):
        return super().search_single_by_columns(email=email)

    def get_by_email_json(self, email: str) -> Response:
        return jsonify( model_to_dict(super().search_by_single_columns(email=email)) )
    
    def get_by_id_json(self, id: int) -> Response:
        return jsonify( model_to_dict(super().get_by_id(obj_id=id, pk_field=self.pk_field)) )
    
    def get_single_value(self, id: int, field_name: str) -> Response:
        '''
            Return the value of a single attribute of the record
        '''
        user = super().search_single_by_columns(id_passeggero = id)
        r = jsonify(model_to_dict(user))
        return r[field_name] 

    def validate_password(self, email: str, password: str) -> bool:
        user = super().search_single_by_columns(email=email)
        
        if user and check_password_hash(user.password, password):
            return True  # Password is correct
        return False  # Password is incorrect