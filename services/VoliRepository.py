import json

from core.VoliClass import VoliClass
from services.BaseRepository import BaseRepository, model_to_dict, to_dict_list
from core.VoliClass import VoliClass

from System import engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from flask import jsonify, Response

from typing import List

from services.BigliettiRepository import BigliettiRepository


class VoliRepository(BaseRepository[VoliClass]):

    def __init__(self):
        super().__init__(VoliClass)
        self.pk_field = "id_volo"

    def add(self,comandante: str, ritardo: str, id_viaggio: str, id_aereo: str,
            id_aereoporto_partenza: str,id_aereoporto_arrivo: str,sequence_identifier:int) -> Response:

        """Create a new Compagnie record (custom wrapper)."""

        rec = super().add(
            comandante = comandante,
            ritardo = ritardo,
            id_viaggio = id_viaggio,
            id_aereo = id_aereo,
            id_aereoporto_partenza = id_aereoporto_partenza,
            id_aereoporto_arrivo = id_aereoporto_arrivo,
            sequence_identifier = sequence_identifier
        )

        if rec is None:
              return jsonify({"success":False})

        return jsonify({"success":True})

    def get_all(self) -> Response:
        """Fetch all Aereoporti records."""
        return jsonify([model_to_dict(aereoporti) for aereoporti in super().get_all()])

    def get_by_id(self, id_volo: str) -> Response:
        """Fetch a single Aereoporti by ID."""
        return jsonify(model_to_dict(super().get_by_id(id_volo, pk_field=self.pk_field),backrefs = True))


    def update(self,id_volo:str,comandante: str, ritardo: str, id_viaggio: str, id_aereo: str,
               id_aereoporto_partenza: str,id_aereoporto_arrivo: str) -> Response:
        """
        Update a Aereoporti.
        kwargs can include email, password, tel, nome, address_id.
        """
        res = super().update(id_volo,
                             self.pk_field,
                             comandante = comandante,
                             ritardo = ritardo,
                             id_viaggio = id_viaggio,
                             id_aereo = id_aereo,
                             id_aereoporto_partenza = id_aereoporto_partenza,
                             id_aereoporto_arrivo = id_aereoporto_arrivo)

        return jsonify({"success":res})

    def delete(self, id_volo: str) -> Response:
        """Delete a Aereoporti by ID."""
        res = super().delete(id_volo, self.pk_field)
        return jsonify({"success":res})

    def get_datatable(self, draw: int, start: int, length: int, search_value: str, id_viaggio: str,**kwargs):

        filter_id_compagnia = kwargs.get('id_compagnia',None)
        params = {"id_viaggio": id_viaggio}

        base_query = '''
                            SELECT sequence_identifier, id_viaggio, COUNT(sequence_identifier) as num_scali, dev."Compagnie".nome as nome_compagnia
                            FROM dev."Voli"
                            LEFT JOIN dev."Aerei" ON dev."Aerei".id_aereo = dev."Voli".id_aereo
                            LEFT JOIN dev."Compagnie" ON dev."Compagnie".id_compagnia = dev."Aerei".id_compagnia
                            WHERE id_viaggio = :id_viaggio'''


        if filter_id_compagnia is not None:
            base_query += ''' AND dev."Aerei".id_compagnia = :id_compagnia'''
            params['id_compagnia'] = filter_id_compagnia
        base_query += ''' GROUP BY sequence_identifier, id_viaggio, dev."Compagnie".nome'''


        query = text(base_query)

        with Session(engine()) as session:
            res = session.execute(query, params).fetchall()

            # Convert rows to dicts
            data = [dict(row._mapping) for row in res]

            return jsonify({
                "draw": draw,
                "recordsTotal": len(res),
                "recordsFiltered": len(res),
                "data": data
            })

        return jsonify({"success": False})

    def get_datatable_details(self, draw: int   , start: int, length: int, search_value: str,sequence_identifier:str):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["nome","citta"],joins=[VoliClass.aereo_rel],sequence_identifier = sequence_identifier)


    def add_from_json(self,voli_json):
        voli = json.loads(voli_json)["tratte"]

        try:
            with Session(engine()) as session:

                sequence_identifier = self.generate_sequence_identifier()+1

                for ordine, volo in enumerate(voli):
                    volo["ordine"] = ordine
                    volo["sequence_identifier"] = sequence_identifier
                    record = self.model(**volo)

                    session.add(record)

                session.commit()
                return jsonify({"success":True})
        except:
            return jsonify({"success":False})

    def delete_all(self, id_viaggio, **kwargs):
        id_compagnia = kwargs.get('id_compagnia', None)

        try:
            with Session(engine()) as session:
                query = session.query(self.model).filter(
                    getattr(self.model, "id_viaggio") == id_viaggio
                )

                if id_compagnia is not None:
                    query = query.join(
                        self.model.aereo_rel  # relazione definita nel modello
                    ).filter(
                        getattr(self.model.aereo_rel, "id_compagnia") == id_compagnia
                    )

                query.delete(synchronize_session=False)
                session.commit()
                return jsonify({"success": True})

        except Exception as e:
            print("Error in delete_all:", e)

        return jsonify({"success": False, "error": str(e)})

    def generate_sequence_identifier(self):
        # get last sequence
        query = text('''
                     SELECT sequence_identifier
                     FROM dev."Voli"
                     ORDER BY sequence_identifier DESC
                         LIMIT 1;
                     ''')

        with Session(engine()) as session:
            res = session.execute(query).fetchall()

        if res:
            return res[0][0]
        return 0

    def get_sequence_by_viaggioDatatable(self, draw: int, start: int, length: int, search_value: str, id_viaggio:str, sequence_identifier:str):
        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["nome","citta"],joins=[VoliClass.aereo_rel],id_viaggio = id_viaggio,sequence_identifier = sequence_identifier)

    def get_sequence_by_viaggio(self,id_viaggio:str, sequence_identifier:str):
        return super().get_all(joins=[VoliClass.aereo_rel,VoliClass.aereoporto_arrivo_rel,VoliClass.aereoporto_partenza_rel],id_viaggio = id_viaggio,sequence_identifier = sequence_identifier)

    def getAllSequenceByViaggio(self,id_andata:str,id_ritorno:str, sequence_identifier_andata:str,sequence_identifier_ritorno:str):


        andata = self.get_sequence_by_viaggio(id_viaggio=id_andata,sequence_identifier=sequence_identifier_andata)
        ritorno = None

        if id_ritorno != 'null' and sequence_identifier_ritorno != 'null':
            ritorno = self.get_sequence_by_viaggio(id_viaggio=id_ritorno,sequence_identifier=sequence_identifier_ritorno)


        biglietti_repo = BigliettiRepository()

        andata_json = [model_to_dict(row,backrefs = True) for row in andata]
        ritorno_json = [model_to_dict(row,backrefs = True) for row in ritorno] if ritorno else []


        for row in andata_json:
            row['seats'] = biglietti_repo.get_by_volo(id_volo=row.get("id_volo"))
            row['prices'] = self.get_prices_per_class(id_volo=row.get("id_volo"))


        for row in ritorno_json:
            row['seats'] = biglietti_repo.get_by_volo(id_volo=row.get("id_volo"))
            row['prices'] = self.get_prices_per_class(id_volo=row.get("id_volo"))

        res = {"andata": andata_json,
               "ritorno": ritorno_json}

        return res

    def get_prices_per_class(self,id_volo):

        query = text('''
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
                                                AND b.id_viaggio = v.id_viaggio
                         WHERE v.id_volo = :id_volo
                         GROUP BY v.id_volo, v.sequence_identifier, amp.seat_class
                     )
                          
                              SELECT
                                  id_volo,
                                  sequence_identifier,
                                  seat_class,
                                  posti_totali,
                                  posti_occupati,
                                  (posti_totali - posti_occupati) AS posti_liberi,
                                  ROUND((posti_occupati::decimal / posti_totali) * 100, 2) AS percentuale_occupati,
                                  CASE
                                      WHEN seat_class = 'Economy'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 50 +100, 2)
                                      WHEN seat_class = 'Business'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 100  +120, 2)
                                      WHEN seat_class = 'FirstClass'::classe THEN ROUND((posti_occupati::decimal / posti_totali) * 200 + 140, 2)
                                      ELSE 0
                                      END AS costo_posto
                              FROM seat_stats
                             WHERE id_volo = :id_volo
                          ''')

        with Session(engine()) as session:
            res = session.execute(query, {
                'id_volo': id_volo
            }).fetchall()

            return to_dict_list(res)

        return connection_err()



