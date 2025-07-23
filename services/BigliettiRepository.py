from __future__ import annotations

from core.BigliettiClass import BigliettiClass
from services.BaseRepository import BaseRepository

from flask import jsonify, Response
from sqlalchemy import text, Row
from System import engine
from sqlalchemy.orm import Session
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
        
        if record is None:
            return jsonify({ "success": False })

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
        
        return jsonify({ 'error': 'Errore di connessione '})
        

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

        return jsonify({ 'error': 'Errore di connessione' })
    
    def get_by_departure(self, id_passeggero: str, partenza: str) -> Response:
        '''
            Return sll the tickets of the given passenger that depart from a given airport's city
            Example: get_by_departure(1, 'Milano')
        '''
        
        query = text('''
                SELECT *
                FROM dev.Biglietti b
                    JOIN dev.Viaggi v USING(id_viaggio)
                    JOIN dev.Aereoporti a ON v.aereoporto_partenza = a.id_aereoporto
                WHERE a.citta = :partenza AND b.id_passeggero = :user
        ''')
        
        with Session(engine()) as session:
            res = session.execute(query, {
                'partenza': partenza,
                'user': id_passeggero
            }).fetchall()

            return json(res, 'Luogo non trovato')
        
        return jsonify({ 'error': 'Errore di connessione' })