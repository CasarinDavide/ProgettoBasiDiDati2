from core.BigliettiClass import BigliettiClass
from services.BaseRepository import BaseRepository, model_to_dict

from flask import jsonify, Response
from sqlalchemy import text
from System import engine
from sqlalchemy.orm import Session

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

    def get_by_user_id(self, id_passeggero) -> Response:
        '''
            Returns all the tickets owned by the given user
        '''
        return jsonify( [model_to_dict(biglietto) for biglietto  in super().search_by_columns(id_passeggero = id_passeggero)] )
    
    def get_by_destination(self, destinazione: str) -> Response:
        query = text('''
                        SELECT a.citta
                        FROM dev.Biglietti b 
                            JOIN dev.Viaggi v USING(id_viaggio)
                            JOIN dev.Aereoporti a ON v.aereoporto_destinazione = a.id_aereoporto 
                        WHERE a.citta = :destinazione
                ''')
        
        with Session(engine()) as session:
            res = session.execute(query, {
                'destinazione': destinazione
            })

            r = [dict(row._mapping) for row in res]
            
            if r:
                return jsonify(r)
            else:
                return jsonify({'error': 'Luogo nei tuoi biglietti non trovato'})

        return jsonify({ 'error': 'Errore di connessione' })
    
    def get_by_departure(self, partenza: str) -> Response:
        r = 0
        return jsonify(r)