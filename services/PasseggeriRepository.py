from sqlalchemy.exc import IntegrityError

from core.PasseggeriClass import PasseggeriClass
from services.BaseRepository import BaseRepository, model_to_dict, connection_err
from datetime import datetime

from flask import jsonify, Response
from werkzeug.security import check_password_hash
from System import engine
from sqlalchemy.orm import SessionTransaction, Session

from services.BigliettiRepository import BigliettiRepository
from services.CompagnieRepository import CompagnieRepository
from services.ViaggiRepository import ViaggiRepository


class PasseggeriRepository(BaseRepository[PasseggeriClass]):
    
    def __init__(self):
        super().__init__(PasseggeriClass)
        self.pk_field = "id_passeggero"
        

    def add(self, email: str, password:str , nome: str, cognome: str, tel: str, nascita: datetime, via: str, civico: str, cod_postale: int, citta: str, paese: str, saldo: float=0) -> Response:
        
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

    def get_by_id(self, id: str,**kwargs):
        return super().search_single_by_columns(id_passeggero=id,**kwargs)
    
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

        try:
            with Session(engine()) as session:
                with session.begin():
                    biglietto = BigliettiRepository.get_biglietto(id_volo=id_andata,seat=posti_andata,session = session)

                    passeggiero = PasseggeriRepository.get_by_id(id_utente,session = session)

                    compagnia_andata = CompagnieRepository.get_by_volo(id_volo=id_andata,session = session)


                    costo_andata = BigliettiRepository.evaluate_price_by_biglietto(biglietto)

                    costo_ritorno = 0
                    compagnia_ritorno = None
                    biglietto_ritorno = None
                    if id_ritorno is not None:
                        compagnia_ritorno = CompagnieRepository.get_by_volo(id_volo=id_ritorno,session = session)
                        biglietto_ritorno = BigliettiRepository.get_biglietto(id_volo=id_andata,seat=posti_andata,session = session)
                        costo_ritorno = BigliettiRepository.evaluate_price_by_biglietto(biglietto_ritorno)

                    total_cost = costo_andata + costo_ritorno

                    if passeggiero.saldo < total_cost:
                        raise ValueError("Insufficient credit")

                    passeggiero.saldo -= total_cost

                    compagnia_andata.saldo += costo_andata

                    if compagnia_ritorno is not None:
                        compagnia_ritorno.saldo += costo_ritorno

                    biglietto.id_passeggiero = id_utente
                    # after this all obj that has reference to internal db will be pushed

        except ValueError as e:
            session.rollback()
            return {"status": "error", "message": str(e)}
        except IntegrityError:
            session.rollback()
            return {"status": "error", "message": "Database integrity error"}
        return {"status": "success", "message": "Tickets purchased successfully"}
