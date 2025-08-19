from services.BaseRepository import BaseRepository, model_to_dict,to_json
from core.ViaggiClass import ViaggiClass

from System import engine
from sqlalchemy.orm import Session
from sqlalchemy import text, Row
from datetime import datetime
from flask import jsonify, Response

from typing import List, Sequence, Any
from datetime import date, time, datetime

from services.VoliRepository import VoliRepository


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

    def add(self,sosta: str, durata: str, id_aereoporto_partenza: str, id_aereoporto_arrivo: str,
            sconto_biglietto: str,data_partenza: str,orario_partenza:str) -> Response:

        """Create a new Compagnie record (custom wrapper)."""

        rec = super().add(
            sosta = sosta,
            durata = durata,
            id_aereoporto_partenza = id_aereoporto_partenza,
            id_aereoporto_arrivo = id_aereoporto_arrivo,
            sconto_biglietto = sconto_biglietto,
            data_partenza = data_partenza,
            orario_partenza = orario_partenza,
        )

        if rec is None:
              return jsonify({"success":False})

        return jsonify({"success":True})

    def get_all(self) -> Response:
        """Fetch all Aereoporti records."""
        return jsonify([model_to_dict(aereoporti) for aereoporti in super().get_all()])

    def get_by_id(self, id_viaggio: str) -> Response:
        """Fetch a single Aereoporti by ID."""
        return jsonify(model_to_dict(super().get_by_id(id_viaggio, pk_field=self.pk_field,joins=[ViaggiClass.partenza_rel,ViaggiClass.arrivo_rel]),backrefs = True))


    def update(self,id_viaggio:str,sosta: str, durata: str, id_aereoporto_partenza: str, id_aereoporto_arrivo: str,
               sconto_biglietto: str,data_partenza: str,orario_partenza:str) -> Response:
        """
        Update a Aereoporti.
        kwargs can include email, password, tel, nome, address_id.
        """
        res = super().update(id_viaggio,
                             self.pk_field,
                             sosta = sosta,
                             durata = durata,
                             id_aereoporto_partenza = id_aereoporto_partenza,
                             id_aereoporto_arrivo = id_aereoporto_arrivo,
                             sconto_biglietto = sconto_biglietto,
                             data_partenza = data_partenza,
                             orario_partenza = orario_partenza)

        return jsonify({"success":res})

    def delete(self, id_viaggio: str) -> Response:
        """Delete a Aereoporti by ID."""
        res = super().delete(id_viaggio, self.pk_field)
        return jsonify({"success":res})

    def get_datatable(self, draw: int   , start: int, length: int, search_value: str):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["nome","citta"],joins=[ViaggiClass.partenza_rel,ViaggiClass.arrivo_rel])

    #TODO : COMMENTATO CONTROLLARE SE HA ROTTO QUALCOSA DI RIKY
    #def get_all(self):
    #    return super().get_all()

    """ Return the List of possible departure """
    def get_list_partenze(self) -> List[str]:
        
        query = text(''' 
                        SELECT DISTINCT a.citta
                        FROM dev."Viaggi" v 
                            JOIN dev."Aereoporti" a ON v.id_aereoporto_partenza = a.id_aereoporto
                        ''')
            # Nel merge mi dava un conflitto questo è il codice vecchio, non so bene il perchè
            # conversione in lista
            #result = [x[0] for x in session.execute(query).all()]
            #return
        
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
    def get_viaggi(self, partenza: str = "", destinazione: str= "", dataP: datetime = None, dataR: datetime= None) -> List[Response]:
        '''
        collection di oggetti json che devono contenere:
            + id_viaggio
            + Durata totale
            + Aereoporto di Partenza
            + Aereoporto di Arrivo
            + Orario di partenza
            + numero di Voli
            + dove arrivano i singoli voli, se ci sono
            + Prezzo del singolo viaggio (quello totale sarà andata + ritorno se c'è)
        '''
        #informazioni sui viaggi ricercati
        query_info_viaggi = text('''

                                 WITH seat_stats AS (
                                     SELECT
                                         v.id_volo,
                                         v.sequence_identifier,
                                         amp.seat_class,
                                         COUNT(*) AS posti_totali,
                                         COUNT(b.id_biglietto) AS posti_occupati
                                     FROM dev."Voli" v
                                              JOIN dev."AereoMappaPosti" amp
                                                   ON amp.id_aereo = v.id_aereo
                                              LEFT JOIN dev."Biglietti" b
                                                        ON b.id_volo = v.id_volo
                                                            AND b.posto = amp.seat_label
                                     GROUP BY v.id_volo, v.sequence_identifier, amp.seat_class
                                 ),
                                      seat_cost AS (
                                          SELECT
                                              id_volo,
                                              sequence_identifier,
                                              seat_class,
                                              posti_totali,
                                              posti_occupati,
                                              (posti_totali - posti_occupati) AS posti_liberi,
                                              ROUND((posti_occupati::decimal / posti_totali) * 100, 2) AS percentuale_occupati,
                                              ---Placeholder to evaluate cost----
                                              CASE
                                                  WHEN seat_class = 'Economy'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 50 +100, 2)
                                                  WHEN seat_class = 'Business'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 100  +120, 2)
                                                  WHEN seat_class = 'FirstClass'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 200 + 140, 2)
                                                  ELSE 0
                                                  END AS costo_minimo
                                          FROM seat_stats
                                      ),
                                      seat_cost_min AS (
                                          SELECT
                                              id_volo,
                                              sequence_identifier,
                                              MIN(costo_minimo) as costo_minimo
                                          FROM seat_cost
                                          GROUP BY id_volo,sequence_identifier
                                      )

                                 SELECT
                                     
                                     v.sequence_identifier,
                                     v.id_viaggio,
                                     viaggi_filtrati.data_partenza AS data_partenza,
                                     viaggi_filtrati.orario_partenza AS orario_partenza,
                                     aereoporto_partenza.citta AS citta_partenza,
                                     aereoporto_partenza.id_aereoporto AS aereoporto_partenza,
                                     aereoporto_arrivo.citta AS citta_destinazione,
                                     aereoporto_arrivo.id_aereoporto AS aereoporto_destinazione,
                                     viaggi_filtrati.durata as durata,
                                     c.nome AS nome_compagnia,
                                     
                                     COUNT(v.sequence_identifier) AS num_scali,
                                     ROUND(SUM((sc.costo_minimo - sc.costo_minimo * COALESCE(viaggi_filtrati.sconto_biglietto, 0))::numeric),2) AS prezzo_biglietto,
                                     STRING_AGG(aereoporto_partenza.nome || ' - ' || aereoporto_arrivo.nome, ' -> ' ORDER BY v.sequence_identifier) AS scali
                                 FROM dev."Voli" v
                                          LEFT JOIN dev."Aerei" a ON a.id_aereo = v.id_aereo
                                          LEFT JOIN dev."Compagnie" c ON c.id_compagnia = a.id_compagnia
                                          LEFT JOIN seat_cost_min sc ON sc.id_volo = v.id_volo
                                          JOIN dev."Viaggi" as viaggi_filtrati ON v.id_viaggio = viaggi_filtrati.id_viaggio
                                          JOIN dev."Aereoporti" AS aereoporto_arrivo ON viaggi_filtrati.id_aereoporto_arrivo = aereoporto_arrivo.id_aereoporto
                                          JOIN dev."Aereoporti" AS aereoporto_partenza ON viaggi_filtrati.id_aereoporto_partenza = aereoporto_partenza.id_aereoporto

                                 WHERE ( aereoporto_partenza.citta = :partenza OR :partenza = '')
                                   AND ( aereoporto_arrivo.citta = :destinazione  OR :destinazione = '')
                                   AND viaggi_filtrati.data_partenza = :dataP

                                 GROUP BY v.sequence_identifier, v.id_viaggio, c.nome,durata,citta_partenza,aereoporto_partenza,citta_destinazione,aereoporto_destinazione,data_partenza,orario_partenza
                                 ORDER BY v.sequence_identifier;

                                
                                ''')

        with Session(engine()) as session:

            rows_andata = session.execute( query_info_viaggi, {
                'partenza': partenza if partenza else "",
                'destinazione': destinazione if destinazione else "",
                'dataP': dataP
            }).fetchall()

            rows_ritorno = ''
            if dataR != '':
                rows_ritorno = session.execute( query_info_viaggi, {
                    'partenza': partenza if partenza else "",
                    'destinazione': destinazione if destinazione else "",
                    'dataP': dataR
                }).fetchall()
            
            andate = json_data(rows_andata)
            ritorni = json_data(rows_ritorno)
            
            res = {}
            trip_counter = 1

            '''
                Raggruppo i risultati della query in modo che risulti il seguente oggetto:
                {
                    1: {
                        'andata': {...},
                        'ritorno: {...}
                    },

                    2: {
                        'andata': {...},
                        'ritorno': {...}
                    },
                    ...
                }

                se il viaggio richiesto è di sola andata:
                {
                    1: {
                        'andata': {...}
                        'ritorno: null
                    },

                    2: {
                        'andata': {...}
                        'ritorno: null
                    }
                }
            '''

            if ritorni:
                for andata in andate:
                    for ritorno in ritorni:
                        res[f'{trip_counter}'] = {
                            'andata': andata,
                            'ritorno': ritorno
                        }
                        trip_counter += 1
            else:
                for andata in andate:
                    res[f'{trip_counter}'] = {
                        'andata': andata,
                        'ritorno': None
                    }
                    trip_counter += 1

            return jsonify(res)


        return jsonify({'error': 'Errore di connessione'})
    def get_viaggi_period(self, dataP: datetime = None, dataR: datetime= None) -> List[Response]:
        '''
        collection di oggetti json che devono contenere:
            + id_viaggio
            + Durata totale
            + Aereoporto di Partenza
            + Aereoporto di Arrivo
            + Orario di partenza
            + numero di Voli
            + dove arrivano i singoli voli, se ci sono
            + Prezzo del singolo viaggio (quello totale sarà andata + ritorno se c'è)
        '''
        #informazioni sui viaggi ricercati
        query_info_viaggi = text('''

                                 WITH seat_stats AS (
                                     SELECT
                                         v.id_volo,
                                         v.sequence_identifier,
                                         amp.seat_class,
                                         COUNT(*) AS posti_totali,
                                         COUNT(b.id_biglietto) AS posti_occupati
                                     FROM dev."Voli" v
                                              JOIN dev."AereoMappaPosti" amp
                                                   ON amp.id_aereo = v.id_aereo
                                              LEFT JOIN dev."Biglietti" b
                                                        ON b.id_volo = v.id_volo
                                                            AND b.posto = amp.seat_label
                                     GROUP BY v.id_volo, v.sequence_identifier, amp.seat_class
                                 ),
                                      seat_cost AS (
                                          SELECT
                                              id_volo,
                                              sequence_identifier,
                                              seat_class,
                                              posti_totali,
                                              posti_occupati,
                                              (posti_totali - posti_occupati) AS posti_liberi,
                                              ROUND((posti_occupati::decimal / posti_totali) * 100, 2) AS percentuale_occupati,
                                              ---Placeholder to evaluate cost----
                                              CASE
                                                  WHEN seat_class = 'Economy'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 50 +100, 2)
                                                  WHEN seat_class = 'Business'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 100  +120, 2)
                                                  WHEN seat_class = 'FirstClass'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 200 + 140, 2)
                                                  ELSE 0
                                                  END AS costo_minimo
                                          FROM seat_stats
                                      ),
                                      seat_cost_min AS (
                                          SELECT
                                              id_volo,
                                              sequence_identifier,
                                              MIN(costo_minimo) as costo_minimo
                                          FROM seat_cost
                                          GROUP BY id_volo,sequence_identifier
                                      )

                                 SELECT

                                     v.sequence_identifier,
                                     v.id_viaggio,
                                     viaggi_filtrati.data_partenza AS data_partenza,
                                     viaggi_filtrati.orario_partenza AS orario_partenza,
                                     aereoporto_partenza.citta AS citta_partenza,
                                     aereoporto_partenza.id_aereoporto AS aereoporto_partenza,
                                     aereoporto_arrivo.citta AS citta_destinazione,
                                     aereoporto_arrivo.id_aereoporto AS aereoporto_destinazione,
                                     viaggi_filtrati.durata as durata,
                                     c.nome AS nome_compagnia,

                                     COUNT(v.sequence_identifier) AS num_scali,
                                     ROUND(SUM((sc.costo_minimo - sc.costo_minimo * COALESCE(viaggi_filtrati.sconto_biglietto, 0))::numeric),2) AS prezzo_biglietto,
                                     STRING_AGG(aereoporto_partenza.nome || ' - ' || aereoporto_arrivo.nome, ' -> ' ORDER BY v.sequence_identifier) AS scali
                                 FROM dev."Voli" v
                                          LEFT JOIN dev."Aerei" a ON a.id_aereo = v.id_aereo
                                          LEFT JOIN dev."Compagnie" c ON c.id_compagnia = a.id_compagnia
                                          LEFT JOIN seat_cost_min sc ON sc.id_volo = v.id_volo
                                          JOIN dev."Viaggi" as viaggi_filtrati ON v.id_viaggio = viaggi_filtrati.id_viaggio
                                          JOIN dev."Aereoporti" AS aereoporto_arrivo ON viaggi_filtrati.id_aereoporto_arrivo = aereoporto_arrivo.id_aereoporto
                                          JOIN dev."Aereoporti" AS aereoporto_partenza ON viaggi_filtrati.id_aereoporto_partenza = aereoporto_partenza.id_aereoporto

                                 WHERE viaggi_filtrati.data_partenza >= :dataP
                                     AND viaggi_filtrati.data_partenza <= :dataR

                                 GROUP BY v.sequence_identifier, v.id_viaggio, c.nome,durata,citta_partenza,aereoporto_partenza,citta_destinazione,aereoporto_destinazione,data_partenza,orario_partenza
                                 ORDER BY v.sequence_identifier;


                                 ''')


        with Session(engine()) as session:

            rows_andata = session.execute( query_info_viaggi, {
                'dataP': dataP,
                'dataR': dataR
            }).fetchall()

            rows_ritorno = ''

            andate = json_data(rows_andata)
            ritorni = json_data(rows_ritorno)

            res = {}
            trip_counter = 1

            '''
                Raggruppo i risultati della query in modo che risulti il seguente oggetto:
                {
                    1: {
                        'andata': {...},
                        'ritorno: {...}
                    },

                    2: {
                        'andata': {...},
                        'ritorno': {...}
                    },
                    ...
                }

                se il viaggio richiesto è di sola andata:
                {
                    1: {
                        'andata': {...}
                        'ritorno: null
                    },

                    2: {
                        'andata': {...}
                        'ritorno: null
                    }
                }
            '''

            if ritorni:
                for andata in andate:
                    for ritorno in ritorni:
                        res[f'{trip_counter}'] = {
                            'andata': andata,
                            'ritorno': ritorno
                        }
                        trip_counter += 1
            else:
                for andata in andate:
                    res[f'{trip_counter}'] = {
                        'andata': andata,
                        'ritorno': None
                    }
                    trip_counter += 1

            return jsonify(res)


        return jsonify({'error': 'Errore di connessione'})
    def get_andata_ritorno(self, id_andata:str, id_ritorno:str):

        res = {}

        res["andata"] = model_to_dict(super().get_by_id(id_andata, pk_field=self.pk_field,joins=[ViaggiClass.partenza_rel,ViaggiClass.arrivo_rel]),backrefs = True)

        if id_ritorno != 'null':
            res["ritorno"] =model_to_dict(super().get_by_id(id_ritorno, pk_field=self.pk_field,joins=[ViaggiClass.partenza_rel,ViaggiClass.arrivo_rel]),backrefs = True)

        return jsonify(res)


