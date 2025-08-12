from __future__ import annotations

from core.BigliettiClass import BigliettiClass
from core.ViaggiClass import ViaggiClass
from services.BaseRepository import BaseRepository, model_to_dict, connection_err

from flask import jsonify, Response
from sqlalchemy import text, Row
from System import engine
from sqlalchemy.orm import Session, joinedload
from typing import Sequence, Any
from datetime import date, time, datetime



def json(rows: Sequence[Row[Any]], error: str) -> Response:
    data = []
    for row in rows:
        row_dict = dict(row._mapping)

        for key, value in row_dict.items():
            if isinstance(value, (date, time, datetime)):
                row_dict[key] = str(value)
        data.append(row_dict)

    if data:
        return jsonify(data)
    else:
        return jsonify({ 'error': error })

class BigliettiRepository(BaseRepository[BigliettiClass]):
    
    def __init__(self):
        super().__init__(BigliettiClass)
        self.pk_field = "id_biglietto"
        

    def add(self, categoria: str, prezzo: str, posto: str, id_viaggio: int, id_passeggero: int | None) -> Response:
        
        record = super.add(
            categoria = categoria,
            prezzo = prezzo,
            posto = posto,
            id_viaggio = id_viaggio,
            id_passeggero = id_passeggero
        )
        
        return jsonify({'succes': (record is not None) })

    def get_by_user(self, id_passeggero: int) -> Response:
        '''
            Returns all the tickets owned by the given user
        '''
        
        query = text('''
                SELECT *    
                    FROM dev."Biglietti" b 
                    JOIN dev."Viaggi" v USING(id_viaggio)
                WHERE b.id_passeggero = :user
        ''')

        with Session(engine()) as session:
            res = session.execute(query, {
                'user': id_passeggero
            }).fetchall()

            return json(res, 'Biglietti non trovati')
        
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

            json(res, 'Luogo non trovato')

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

            return json(res, 'Luogo non trovato')
        
        return connection_err()
    
    def get_by_viaggio(self, id_viaggio: str) -> Response:
        '''
            Return all the tickets of the given trip that are not already taken
        '''
        query = text('''
            SELECT b.categoria AS categoria, b.prezzo AS prezzo, b.posto AS posto
            FROM dev."Biglietti" b
            WHERE b.id_viaggio = :id_viaggio AND b.id_passeggero IS NULL
        ''')

        with Session(engine()) as session:
            res = session.execute(query, {
                'id_viaggio': id_viaggio
            }).fetchall()

            return json(res, 'Errore nell\'elaborazione dei biglietti')
        
        return connection_err()
    
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
            return json(res, 'Errore nell\'elaborazione dei biglietti')
        
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

    def get_biglietto(self,id_volo,seat,**kwargs):
        return self.search_by_columns(joins=[joinedload(BigliettiClass.viaggio_rel).joinedload(ViaggiClass.voli_rel)],id_volo = id_volo,posto = seat,**kwargs)

    def set_seat(self,id_biglietto,id_passeggiero):
        # it cannot fail must assume existing biglietto is passed
        super().update(obj_id=id_biglietto,pk_field=self.pk_field,id_passeggiero = id_passeggiero)
