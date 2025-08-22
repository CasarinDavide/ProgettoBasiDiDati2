from __future__ import annotations

from typing import Literal

import jsons
from sqlalchemy.exc import SQLAlchemyError

from core.BigliettiClass import BigliettiClass, CategoriaEnum
from core.ViaggiClass import ViaggiClass
from services.BaseRepository import BaseRepository, model_to_dict, connection_err, to_dict_list, to_json

from flask import jsonify, Response, json
from sqlalchemy import text, Row
from System import engine
from sqlalchemy.orm import Session, joinedload


CategoriaType = Literal['Economy', 'Business', 'FirstClass']
class BigliettiRepository(BaseRepository[BigliettiClass]):
    
    def __init__(self):
        super().__init__(BigliettiClass)
        self.pk_field = "id_biglietto"
        

    def add(self, categoria: str, prezzo: str, posto: str, id_viaggio: str, id_passeggero: str | None,nome:str,cognome:str,id_volo:str,**kwargs) -> Response:
        
        record = super().add(
            categoria = categoria,
            prezzo = prezzo,
            posto = posto,
            id_viaggio = id_viaggio,
            id_passeggero = id_passeggero,
            nome=nome,
            cognome=cognome,
            id_volo = id_volo,
            **kwargs
        )
        
        return jsonify({'succes': (record is not None) })

    def get_by_user(self, id_passeggero: int) -> Response:
        '''
            Returns all the tickets owned by the given user
        '''
        
        query = text('''
                SELECT *
                FROM dev."Biglietti" b 
                WHERE b.id_passeggero = :user
        ''')

        with Session(engine()) as session:
            res = session.execute(query, {
                'user': id_passeggero
            }).fetchall()

            return to_json(res, 'Biglietti non trovati')
        
        return connection_err()
        

    def get_by_destination(self, id_passeggero: int, destinazione: str) -> Response:
        '''
            Returns all the tickets of the given passenger that go to a given destination
            Example: get_by_destination(1, 'Barcellona')
        '''
        query = text('''
                SELECT *
                FROM dev.Biglietti b 
                    JOIN dev.Viaggi v USING(id_viaggio)
                    JOIN dev.Aereoporti a ON v.aereoporto_destinazione = a.id_aereoporto 
                WHERE a.citta = :destinazione AND b.id_passeggero = :user
        ''')
        
        with Session(engine()) as session:
            res = session.execute(query, {
                'destinazione': destinazione,
                'user': id_passeggero
            }).fetchall()

            to_json(res, 'Luogo non trovato')

        return connection_err()
    
    def get_by_departure(self, id_passeggero: str, partenza: str) -> Response:
        '''
            Return all the tickets of the given passenger that depart from a given airport's city
            Example: get_by_departure(1, 'Milano')
        '''
        
        query = text('''
                SELECT *
                FROM dev."Biglietti" b
                    JOIN dev."Viaggi" v USING(id_viaggio)
                    JOIN dev."Aereoporti" a ON v.aereoporto_partenza = a.id_aereoporto
                WHERE a.citta = :partenza AND b.id_passeggero = :user
        ''')
        
        with Session(engine()) as session:
            res = session.execute(query, {
                'partenza': partenza,
                'user': id_passeggero
            }).fetchall()

            return to_json(res, 'Luogo non trovato')
        
        return connection_err()
    
    def get_by_viaggio(self, id_viaggio: str) -> Response:
        '''
            Return all the tickets of the given trip
        '''
        return None
    
    def get_occupied_seats(self, id_viaggio: str) -> Response:
        '''
            Return all occupied seats of a given trip
        '''

        query = text('''
            SELECT b.posto AS posto
            FROM dev."Biglietti" b
            WHERE b.id_viaggio = :id_viaggio AND b.id_passeggero IS NOT NULL
        ''')

        with Session(engine()) as session:
            res = session.execute(query, {
                'id_viaggio': id_viaggio
            }).fetchall()
            return to_json(res, 'Errore nell\'elaborazione dei biglietti')
        
        return connection_err()

    def get_price(self,id_volo,seat):
        biglietto = self.search_by_columns(joins=[joinedload(BigliettiClass.viaggio_rel).joinedload(ViaggiClass.voli_rel)],id_volo = id_volo,posto = seat)
        if biglietto is not None:
            return biglietto.prezzo * biglietto.viaggio_rel.sconto
        else:
            return -100

    def evaluate_price_by_biglietto(self,biglietto:BigliettiClass):

        if biglietto.viaggio_rel is not None:
            return biglietto.prezzo * biglietto.viaggio_rel.sconto
        else:
            # should not be used, I expect to have viaggio_rel not null
            return biglietto.prezzo

    def get_biglietto(self, id_volo, seat,**kwargs):
        return self.search_by_columns(joins=[joinedload(BigliettiClass.viaggio_rel).joinedload(ViaggiClass.voli_rel)],id_volo = id_volo,posto = seat,**kwargs)

    def set_seat(self,id_biglietto,id_passeggero):
        # it cannot fail must assume existing biglietto is passed
        super().update(obj_id=id_biglietto,pk_field=self.pk_field,id_passeggero = id_passeggero)


    def get_by_volo(self, id_volo):
        query = text('''
                     SELECT mappa_posti.*, CASE WHEN seat_label NOT IN (SELECT posto 
                                                                        FROM "dev"."Biglietti" 
                                                                        WHERE id_viaggio = 1 
                                                                          AND "dev"."Biglietti".categoria = seat_class) THEN 0 ELSE 1 END AS posti_occupati,
                            CASE
                                WHEN seat_class = 'Business' THEN 1
                                WHEN seat_class = 'Economy' THEN 0
                                ELSE 3
                                END AS class_order
                     FROM "dev"."AereoMappaPosti" as mappa_posti
                     JOIN "dev"."Voli" as v ON v.id_volo = :id_volo AND mappa_posti.id_aereo = v.id_aereo
                     WHERE id_volo = :id_volo
                     ORDER BY class_order DESC,
                              CAST(mappa_posti.seat_row AS INT),
                              CAST(mappa_posti.seat_column AS INT);
                     ''')

        with Session(engine()) as session:
            res = session.execute(query, {
                'id_volo': id_volo
            }).fetchall()

            return to_dict_list(res)

        return connection_err()

    def checkout(self, id_andata:str, id_ritorno:str, quantity:str, json_data:str,id_passeggero):
        """
            json_data structure example:
            [
                {
                    'nome': 'Davide',
                    'cognome': 'Casarin',
                    'cabin': 'Business',
                    'seat': '2D',
                    'travelType': 'andata',
                    'route': 'Milano -> Frankfurt am Main',
                    'volo_raw_data': {...},
                    'price': 120.0
                },
                ...
            ]
            """
        data = json.loads(json_data)

        try:
            with Session(engine()) as session:
                with session.begin():  # transaction
                    for biglietto in data:
                        # Determine if it's the outbound or return flight
                        id_viaggio = id_andata if biglietto.get('travelType') == 'andata' else id_ritorno

                        # Add the ticket
                        record = self.add(
                            categoria=CategoriaEnum(biglietto.get('cabin')),
                            prezzo=float(biglietto.get('price')),
                            id_viaggio=int(id_viaggio),
                            id_passeggero=int(id_passeggero),
                            posto=biglietto.get('seat'),
                            nome=biglietto.get('nome'),
                            cognome=biglietto.get('cognome'),
                            id_volo=biglietto.get('volo_raw_data', {}).get('id_volo'),
                            session=session
                        )

                        if record is None:
                            raise ValueError(f"Failed to create ticket for {biglietto.get('nome')} {biglietto.get('cognome')}")

            return jsonify({"success": True, "message": ""})

        except (SQLAlchemyError, ValueError) as e:
            print(e)
            return jsonify({"success": False})




