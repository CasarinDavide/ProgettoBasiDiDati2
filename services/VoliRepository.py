import json

from core.VoliClass import VoliClass
from services.BaseRepository import BaseRepository, model_to_dict
from core.VoliClass import VoliClass

from System import engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from flask import jsonify, Response

from typing import List

class VoliRepository(BaseRepository[VoliClass]):

    def __init__(self):
        super().__init__(VoliClass)
        self.pk_field = "id_volo"

    def add(self,comandante: str, ritardo: str, id_viaggio: str, id_aereo: str,
            id_aereoporto_partenza: str,id_aereoporto_arrivo: str) -> Response:

        """Create a new Compagnie record (custom wrapper)."""

        rec = super().add(
            comandante = comandante,
            ritardo = ritardo,
            id_viaggio = id_viaggio,
            id_aereo = id_aereo,
            id_aereoporto_partenza = id_aereoporto_partenza,
            id_aereoporto_arrivo = id_aereoporto_arrivo
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

    def get_datatable(self, draw: int   , start: int, length: int, search_value: str,id_viaggio:str):

        return super().get_datatable(draw=draw,
                                     start=start,
                                     length=length,
                                     search_value=search_value,
                                     search_fields=["nome","citta"],joins=[VoliClass.aereo_rel],id_viaggio = id_viaggio)

    def add_from_json(self,voli_json):
        voli = json.loads(voli_json)["tratte"]

        try:
            with Session(engine()) as session:
                for ordine, volo in enumerate(voli):
                    volo["ordine"] = ordine
                    record = self.model(**volo)
                    session.add(record)

                session.commit()
                return jsonify({"success":True})
        except:
            return jsonify({"success":False})

    def delete_all(self, id_viaggio):
        try:
            with Session(engine()) as session:
                session.query(self.model).filter(
                    getattr(self.model, "id_viaggio") == id_viaggio
                ).delete(synchronize_session=False)

                session.commit()
                return jsonify({"success": True})
        except Exception as e:
            print("Error in delete_all:", e)
            return jsonify({"success": False, "error": str(e)})

