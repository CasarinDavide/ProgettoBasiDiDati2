from typing import Optional, List, Type, TypeVar, Generic, Any, Dict
from flask import jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from System import engine

# Define a generic type for SQLAlchemy models
T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def add(self, **kwargs) -> Optional[T]:
        """Create a new record for the model."""
        try:
            with Session(engine()) as session:
                record = self.model(**kwargs)
                session.add(record)
                session.commit()
                session.refresh(record)
                return record
        except SQLAlchemyError as e:
            print(f"Error adding record: {e}")
            return None

    def get_all(self) -> List[T]:
        """Fetch all records."""
        with Session(engine()) as session:
            return session.query(self.model).all()

    def get_by_id(self, obj_id: int, pk_field: str = "id") -> Optional[T]:
        """Fetch a single record by primary key."""
        with Session(engine()) as session:
            return session.query(self.model).filter(getattr(self.model, pk_field) == obj_id).first()

    def update(self, obj_id: int, pk_field: str = "id", **kwargs) -> bool:
        """Update a record by ID."""
        with Session(engine()) as session:
            obj = session.query(self.model).filter(getattr(self.model, pk_field) == obj_id).first()
            if not obj:
                return False
            for key, value in kwargs.items():
                setattr(obj, key, value)
            session.commit()
            return True

    def delete(self, obj_id: int, pk_field: str = "id") -> bool:
        """Delete a record by ID."""
        with Session(engine()) as session:
            obj = session.query(self.model).filter(getattr(self.model, pk_field) == obj_id).first()
            if not obj:
                return False
            session.delete(obj)
            session.commit()
            return True

    def get_datatable(
            self,
            draw: int,
            start: int,
            length: int,
            search_value: str,
            search_fields: List[str]
    ):
        """
        Generic DataTable query with search.
        search_fields: list of model fields to search (like ['nome', 'email', 'tel'])
        """
        with Session(engine()) as session:
            query = session.query(self.model)
            records_total = query.count()

            if search_value:
                filters = [
                    getattr(self.model, field).ilike(f"%{search_value}%")
                    for field in search_fields
                ]
                query = query.filter(or_(*filters))

            records_filtered = query.count()
            rows = query.offset(start).limit(length).all()

            # Convert rows to simple lists
            data = [
                [getattr(r, field) for field in search_fields]
                for r in rows
            ]

        return jsonify({
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data
        })
