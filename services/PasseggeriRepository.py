from core.PasseggeriClass import PasseggeriClass
from services.BaseRepository import BaseRepository, model_to_dict, connection_err
from datetime import datetime

from flask import jsonify, Response
from werkzeug.security import check_password_hash
from System import engine
from sqlalchemy.orm import SessionTransaction



class PasseggeriRepository(BaseRepository[PasseggeriClass]):
    
    def __init__(self):
        super().__init__(PasseggeriClass)
        self.pk_field = "id_passeggero"
        

    def add(self, email: str, password:str , nome: str, cognome: str, tel: str, nascita: datetime, saldo: float, via: str, civico: str, cod_postale: int, citta: str, paese: str) -> Response:
        
        record = super().add(
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
        else:
            return jsonify({ "success": True })

    def get_all(self) -> Response:
        return jsonify( [model_to_dict(passeggero) for passeggero in super().get_all()] )

    def get_by_id(self, id: str):
        return super().search_single_by_columns(id_passeggero=id)
    
    def get_by_email(self, email: str):
        return super().search_single_by_columns(email=email)

    def get_by_email_json(self, email: str) -> Response:
        return jsonify( model_to_dict(super().search_single_by_columns(email=email)) )
    
    def get_by_id_json(self, id: int) -> Response:
        return jsonify( model_to_dict(super().get_by_id(obj_id=id, pk_field=self.pk_field)) )
    
    def get_single_attribute(self, id: int, field_name: str) -> Response:
        '''
            Return the value of a single attribute of the user's record
        '''
        user = super().search_single_by_columns(id_passeggero = id)
        r = jsonify(model_to_dict(user))
        return r

    def validate_password(self, email: str, password: str) -> bool:
        user = super().search_single_by_columns(email=email)
        
        if user and check_password_hash(user.password, password):
            return True  # Password is correct
        return False  # Password is incorrect
    
    def buy_tickets(self, id_utente: str, id_andata: str, id_ritorno: str, posti_andata: list[str], posti_ritorno: list[str], quantita: int):
        
        #per info, i posti sono passati come: ['4C:Nome Cognome', '3E:Riccardo Pasinato']

        #TODO implementare la transazione. Ad alto livello bisogna:
        #controllare il credito dell'utente
        #sottrarre il credito e aggiungerlo alla compagnia aerea (bisogna aggiungere un campo alla compagnia aerea dove mettere i soldi)
        #assegnare i biglietti all'utente che ha effettuato l'acquisto
        #assegnare ad ogni biglietto il nominativo inserito dall'utente che ha effettuato gli acquisti
        return