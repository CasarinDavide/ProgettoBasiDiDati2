from services.BaseRepository import BaseRepository
from services.BigliettiRepository import json
from core.ViaggiClass import ViaggiClass

from System import engine
from sqlalchemy.orm import Session
from sqlalchemy import text, Row
from datetime import datetime
from flask import jsonify, Response

from typing import List, Sequence, Any
from datetime import date, time, datetime

def json_data(rows: Sequence[Row[Any]]) -> List:
    """Converte le righe in lista di dizionari, senza response"""
    data = []
    for row in rows:
        row_dict = dict(row._mapping)
        for key, value in row_dict.items():
            if isinstance(value, (date, time, datetime)):
                row_dict[key] = str(value)
        data.append(row_dict)
    return data

class ViaggiRepository(BaseRepository[ViaggiClass]):

    def __init__(self):
        super().__init__(ViaggiClass)
        self.pk_field = "id_viaggio"

    def get_all(self):
        return super().get_all()

    """ Return the List of possible departure """
    def get_list_partenze(self) -> List[str]:
        
        query = text(''' 
                        SELECT DISTINCT a.citta
                        FROM dev."Viaggi" v 
                            JOIN dev."Aereoporti" a ON v.id_aereoporto_partenza = a.id_aereoporto
                        ''')
        
        with Session(engine()) as session:
            rows = session.execute(query).fetchall()
            
            return [row[0] for row in rows]

        return None

    """ Return the List of possible destinations """
    def get_list_arrivi(self) -> List[str]:
        query = text(''' 
                    SELECT DISTINCT a.citta
                    FROM dev."Viaggi" v 
                        JOIN dev."Aereoporti" a ON v.id_aereoporto_arrivo = a.id_aereoporto
                    ''')
        
        with Session(engine()) as session:
            rows = session.execute(query).fetchall()
            
            return [row[0] for row in rows]
        return None
    
    """ select all trips with given parameters and all their informations """
    def get_viaggi(self, partenza: str, destinazione: str, dataP: datetime, dataR: datetime, biglietto: str) -> List[Response]:
        '''
        collection di oggetti json che devono contenere:
            + id_viaggio
            + Durata totale
            + Aereoporto di Partenza
            + Aereoporto di Arrivo
            + Orario di partenza
            + numero di Voli
            - dove arrivano i singoli voli, se ci sono
            + Prezzo del singolo viaggio (quello totale sarà andata + ritorno se c'è)
        '''
        #informazioni sui viaggi ricercati
        query_info_viaggi = text('''
                                WITH viaggi_dettagli AS (
                                    SELECT 
                                        v.id_viaggio AS id_viaggio,
                                        v.durata AS durata, 
                                        prt.citta AS citta_partenza, 
                                        dst.citta AS citta_destinazione,
                                        v.data_partenza AS data_partenza,
                                        v.orario_partenza AS orario_partenza

                                    FROM dev."Viaggi" v 
                                        JOIN dev."Aereoporti" prt ON v.id_aereoporto_partenza = prt.id_aereoporto     
                                        JOIN dev."Aereoporti" dst ON v.id_aereoporto_arrivo = dst.id_aereoporto                                    
                                    WHERE prt.citta = :partenza AND dst.citta = :destinazione AND v.data_partenza = :dataP
                                ),

                                costo_biglietto AS (
                                    SELECT 
                                        v.id_viaggio AS id_viaggio, 
                                        MIN(b.prezzo) AS prezzo
                                    
                                    FROM dev."Biglietti" b 
                                        JOIN viaggi_dettagli v USING(id_viaggio)
                                    
                                    WHERE b.categoria = :biglietto 
                                    GROUP BY v.id_viaggio
                                ),

                                numero_scali_intermedi AS (
                                    SELECT 
                                        v.id_viaggio AS id_viaggio, 
                                        COUNT(*) AS numero_scali
                                    
                                    FROM dev."Voli" voli 
                                        JOIN viaggi_dettagli v USING(id_viaggio)
                                    
                                    GROUP BY v.id_viaggio
                                ),
                                 
                                info_scali AS (
                                    SELECT 
                                        vo.id_viaggio AS id_viaggio,
                                        vo.ordine AS ordine, 
                                        a.citta AS citta
                                    FROM dev."Viaggi" vi 
                                        JOIN dev."Voli" vo USING(id_viaggio)
                                        JOIN dev."Aereoporti" a ON vo.id_aereoporto_arrivo = a.id_aereoporto
                                    WHERE vo.ordine <> 1
                                    ORDER BY vo.ordine
                                ),

                                info_scali_aggregati AS (
                                    SELECT
                                        vo.id_viaggio AS id_viaggio,
                                        STRING_AGG(a.citta, ', ' ORDER BY vo.ordine) AS scali
                                    FROM dev."Viaggi" vi
                                        JOIN dev."Voli" vo USING(id_viaggio)
                                        JOIN dev."Aereoporti" a ON vo.id_aereoporto_arrivo = a.id_aereoporto
                                    WHERE vo.ordine <> 1
                                    GROUP BY vo.id_viaggio
                                )
                                SELECT
                                    vd.id_viaggio AS id_viaggio,
                                    vd.durata AS durata,
                                    vd.citta_partenza AS citta_partenza,
                                    vd.citta_destinazione AS citta_destinazione,
                                    vd.data_partenza AS data_partenza,
                                    cb.prezzo AS prezzo_biglietto,
                                    si.numero_scali AS numero_scali,
                                    COALESCE(isa.scali, 'Nessuno scalo') AS scali
                                
                                FROM viaggi_dettagli vd
                                    JOIN costo_biglietto cb USING(id_viaggio)
                                    JOIN numero_scali_intermedi si USING(id_viaggio)
                                    LEFT JOIN info_scali_aggregati isa USING(id_viaggio);
                                ''')

        with Session(engine()) as session:
            rows_andata = session.execute( query_info_viaggi, {
                'partenza': partenza,
                'destinazione': destinazione,
                'dataP': dataP,
                'biglietto': biglietto
            }).fetchall()

            rows_ritorno = ''
            if dataR != '':
                rows_ritorno = session.execute( query_info_viaggi, {
                    'partenza': destinazione,
                    'destinazione': partenza,
                    'dataP': dataR,
                    'biglietto': biglietto
                }).fetchall()
            
            andate = json_data(rows_andata)
            ritorni = json_data(rows_ritorno)
            
            res = {}
            trip_counter = 1

            '''
                Raggruppo i risultati della query in modo che risulti il seguente oggetto:
                {
                    trip1: {
                        'andata': {},
                        'ritorno: {}
                    },

                    trip2: {
                        'andata': {...},
                        'ritorno': {...}
                    },
                    ...
                }

                se il viaggio richiesto è di sola andata:
                {
                    trip1: {
                        'andata': {...}
                        'ritorno: ''
                    },

                    trip2: {
                        'andata': {...}
                        'ritorno: ''
                    }
                }
            '''

            if ritorni:
                for andata in andate:
                    for ritorno in ritorni:
                        res[f'trip{trip_counter}'] = {
                            'andata': andata,
                            'ritorno': ritorno
                        }
                        trip_counter += 1
            else:
                for andata in andate:
                    res[f'trip{trip_counter}'] = {
                        'andata': andata,
                        'ritorno': ''
                    }
                    trip_counter += 1

            return jsonify(res)


        return jsonify({'error': 'Errore di connessione'})
            