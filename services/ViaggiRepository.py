from services.BaseRepository import BaseRepository, model_to_dict
from core.ViaggiClass import ViaggiClass

from System import engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from flask import jsonify

from typing import Optional, List

class ViaggiRepository(BaseRepository[ViaggiClass]):

    def __init__(self):
        super().__init__(ViaggiClass)
        self.pk_field = "id_viaggio"

    def get_all(self):
        return super().get_all()

    """ Return the List of possible departure """
    def get_list_partenze(self) -> List[str]:
        with Session(engine()) as session:
            query = text(''' 
                        SELECT DISTINCT a.citta
                        FROM dev."Viaggi" v 
                            JOIN dev."Aereoporti" a ON v.id_aereoporto_partenza = a.id_aereoporto
                        ''')
            # conversione in lista
            result = [x[0] for x in session.execute(query).all()]
            return 

        return None

    """ Return the List of possible destinations """
    def get_list_arrivi(self) -> List[str]:
        with Session(engine()) as session:
            query = text(''' 
                        SELECT DISTINCT a.citta
                        FROM dev."Viaggi" v 
                            JOIN dev."Aereoporti" a ON v.id_aereoporto_arrivo = a.id_aereoporto
                        ''')
            # converto Sequence[Row[Any]] in un List[dict]
            res = [x[0] for x in session.execute(query).all()]
            return res
        return None
    
    """ select all trips with given parameters and all their informations """
    def get_viaggi(self, partenza: str, destinazione: str, dataP: datetime, dataR: datetime, biglietto: str):
        '''
        collection di oggetti json che devono contenere:
            - id_viaggio
            - Durata totale
            - Aereoporto di Partenza
            - Aereoporto di Arrivo
            - Orario di partenza
            - Orario di arrivo previsto
            - numero di Voli
            - dove arrivano i singoli voli, se ci sono
            - Prezzo del viaggio
        '''
        #non penso funzioni
        query = text('''
                WITH viaggi_dettagli AS (
                    SELECT 
                        v.id_viaggio,
                        v.durata, 
                        prt.citta, 
                        dst.citta,
                        d.data

                    FROM dev."Viaggi" v 
                        JOIN dev."Aereoporti" prt ON v.id_aereoporto_partenza = prt.id_aereoporto     
                        JOIN dev."Aereoporti" dst ON v.id_aereoporto_arrivo = dst.id_aereoporto
                        JOIN dev."DataPartenze" d USING(id_viaggio)
                    
                    WHERE prt.citta = :partenza AND dst.citta = :destinazione AND d.data = :dataP
                ),

                costo_biglietto AS (
                    SELECT v.id_viaggio, MIN(b.prezzo)
                    FROM dev."Biglietti" b JOIN viaggi_dettagli v USING(id_viaggio)
                    WHERE b.categoria = :biglietto 
                    GROUP BY v.id_viaggio
                ),
                
                numero_scali_intermedi AS (
                    SELECT v.id_viaggio, COUNT(*)
                    FROM dev."Voli" voli JOIN viaggi_dettagli v USING(id_viaggio)
                    GROUP BY v.id_viaggio
                )

                SELECT *
                FROM viaggi_dettagli vd
                    JOIN costo_biglietto cb USING(id_viaggio)
                    JOIN numero_scali_intermedi si USING(id_viaggio)
                ''')
        
        with Session(engine()) as session:
            res_andata = session.execute( query, {
                'partenza': partenza,
                'destinazione': destinazione,
                'dataP': dataP,
                'biglietto': biglietto
            })

            res_ritorno = session.execute( query, {
                'partenza': destinazione,
                'destinazione': partenza,
                'dataP': dataR,
                'biglietto': biglietto
            })

        andata1 = {
            "id_viaggio": "1",
            "aereoporto_partenza": "Venezia",
            "orario_partenza": "8:45",
            "aereoporto_arrivo": "Barcellona",
            "orario_arrivo": "10:45",
            "durata": "2h",
            "numero_voli": 1,
            "destinazioni_voli": [],
            "prezzo": 259.65
        }

        ritorno1 = {
            "id_viaggio": "1",
            "aereoporto_partenza": "Barcellona",
            "orario_partenza": "8:45",
            "aereoporto_arrivo": "Venezia",
            "orario_arrivo": "10:55",
            "durata": "2h 10min",
            "numero_voli": 2,
            "destinazioni_scali": ['Parigi'],
            "prezzo": 259.65
        }

        andata2 = {
            "id_viaggio": "2",
            "aereoporto_partenza": "Venezia",
            "orario_partenza": "8:45",
            "aereoporto_arrivo": "Barcellona",
            "orario_arrivo": "10:45",
            "durata": "10h 15min",
            "numero_voli": 1,
            "destinazioni_scali": [],
            "prezzo": 259.65
        }
        
        ritorno2 = {
            "id_viaggio": "2",
            "aereoporto_partenza": "Venezia",
            "orario_partenza": "8:45",
            "aereoporto_arrivo": "Barcellona",
            "orario_arrivo": "10:45",
            "durata": "10h 15min",
            "numero_voli": 1,
            "destinazioni_voli": [],
            "prezzo": 259.65
        }

        return [
            [andata1, ritorno1],
            [andata2, ritorno2]
            ]