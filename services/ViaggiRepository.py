from services.BaseRepository import BaseRepository
from core.ViaggiClass import ViaggiClass
from core.AereoportiClass import AereoportiClass

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
                        SELECT DISTINCT i.citta
                        FROM dev."Viaggi" v JOIN dev."Aereoporti" a ON v.id_aereoporto_partenza = a.id_aereoporto JOIN dev."Indirizzi" i USING(address_id)
                        ''')
            
            result = session.execute(query).all()
            return result
        return None

    """ Return the List of possible destinations """
    def get_list_arrivi(self) -> List[str]:
        with Session(engine()) as session:
            query = text(''' 
                        SELECT DISTINCT i.citta
                        FROM dev."Viaggi" v JOIN dev."Aereoporti" a ON v.id_aereoporto_arrivo = a.id_aereoporto JOIN dev."Indirizzi" i USING(address_id)
                        ''')
            
            return session.execute(query).all()
    
    """ select all trips with given parameters and all their informations """
    def get_viaggi(self, partenza: str, destinazione: str, dataP: datetime, dataR: datetime, biglietto: str):
        '''
        collection di oggetti json che devono contenere:
            1 - id_viaggio
            1 - Durata totale
            1 - Aereoporto di Partenza
            1 - Aereoporto di Arrivo
            1 - Orario di partenza
            - Orario di arrivo previsto
            - numero di Voli
            - dove arrivano i singoli voli, se ci sono
            - Prezzo del viaggio
        '''
        #non penso funzioni
        query = '''
                WITH viaggi_dettagli AS (
                    SELECT 
                        v.id_viaggio,
                        v.durata, 
                        i_prt.citta, 
                        i_dst.citta,
                        d.data

                    FROM dev."Viaggi" v 
                        JOIN dev."Aereoporti" prt ON v.id_aereoporto_partenza = prt.id_aereoporto 
                        JOIN dev."Indirizzi" i_prt ON prt.address_id = i_prt.address_id        
                        JOIN dev."Aereoporti" dst ON v.id_aereoporto_arrivo = dst.id_aereoporto
                        JOIN dev."Indirizzi" i_dst ON dst.address_id = i_dst.address_id
                        JOIN dev."DataPartenze" d USING(id_viaggio)
                    
                    WHERE i_prt = partenza AND i_dst = destinazione AND d.data = dataP
                ),

                WITH costo_biglietto AS (
                    SELECT v.id_viaggio, MIN(b.prezzo)
                    FROM dev."Biglietti" b JOIN viaggi_dettagli v ON
                    WHERE b.categoria = biglietto 
                    GROUP BY v.id_viaggio
                ),
                
                WITH scali_intermedi AS (
                    SELECT v.id_viaggio, COUNT(*)
                    FROM dev."Voli" voli JOIN viaggi_dettagli v USING(id_viaggio)
                    GROUP BY v.id_viaggio
                )

                SELECT *
                FROM viaggi_dettagli vd
                    JOIN costo_biglietto cb USING(id_viaggio)
                    JOIN scali_intermedi si USING(id_viaggio)
                '''
        
        stmt = text(query, {
            'partenza': partenza,
            'destinazione': destinazione,
            'dataP': dataP,
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