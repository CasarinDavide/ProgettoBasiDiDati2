import datetime
from typing import Optional, List, Type, TypeVar, Generic, Any, Dict
from flask import jsonify
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, inspect
from System import engine

T = TypeVar("T")

from sqlalchemy.inspection import inspect

from sqlalchemy.inspection import inspect
from sqlalchemy.orm.state import InstanceState

def model_to_dict(obj, include_relationships=True, backrefs=False):
    """Convert SQLAlchemy model instance to dict, avoiding DetachedInstanceError"""
    mapper = inspect(obj.__class__)
    state: InstanceState = inspect(obj)
    data = {}

    # Extract basic columns
    for c in mapper.columns:
        value = getattr(obj, c.key)
        if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
            data[c.key] = value.isoformat()
        else:
            data[c.key] = value

    if include_relationships:
        for rel in mapper.relationships:
            if not backrefs and rel.back_populates:
                continue

            if rel.key in state.unloaded:
                continue

            value = getattr(obj, rel.key)

            if value is None:
                data[rel.key] = None
            elif rel.uselist:
                # For one-to-many / many-to-many → list of objects
                data[rel.key] = [
                    model_to_dict(item, include_relationships=False) for item in value
                ]
            else:
                # For many-to-one / one-to-one → single object
                data[rel.key] = model_to_dict(value, include_relationships=False)

    return data


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def _apply_joins(self, query, joins: Optional[List[Any]] = None):
        """Helper to apply joins dynamically"""
        if joins:

            for j in joins:
                # joinedload is useful bc doesnt filter row based on join
                # but add information about ext table
                query = query.options(joinedload(j))
        return query

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

    def get_all(self, joins: Optional[List[Any]] = None,**kwargs) -> List[T]:
        """Fetch all records, with optional joins."""
        with Session(engine()) as session:
            query = session.query(self.model)
            if joins:
                for j in joins:
                    query = query.options(joinedload(j))

            filters = [getattr(self.model, key) == value for key, value in kwargs.items()]
            query = query.filter(and_(*filters))

            return query.all()

    def get_by_id(self, obj_id, pk_field: str = "id", joins: Optional[List[Any]] = None) -> Optional[T]:
        """Fetch a single record by primary key, with optional joins."""
        with Session(engine()) as session:
            query = session.query(self.model)
            if joins:
                for j in joins:
                    query = query.options(joinedload(j))
            query = query.filter(getattr(self.model, pk_field) == obj_id)
            print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
            return query.first()

    def update(self, obj_id, pk_field: str = "id", **kwargs) -> bool:
        """Update a record by ID."""
        with Session(engine()) as session:
            obj = session.query(self.model).filter(getattr(self.model, pk_field) == obj_id).first()
            if not obj:
                return False
            for key, value in kwargs.items():
                setattr(obj, key, value)
            session.commit()
            return True

    def delete(self, obj_id, pk_field: str = "id") -> bool:
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
            search_fields: List[str],
            joins: Optional[List[Any]] = None,
            **kwargs
    ):
        """
        Generic DataTable query with search + optional joins.
        search_fields: list of model fields to search (like ['nome', 'email', 'tel'])
        """
        with Session(engine()) as session:
            query = session.query(self.model)
            query = self._apply_joins(query, joins)

            records_total = query.count()

            if search_value:
                filters = [
                    getattr(self.model, field).ilike(f"%{search_value}%")
                    for field in search_fields
                ]
                query = query.filter(or_(*filters))


            filters = [getattr(self.model, key) == value for key, value in kwargs.items()]
            query = query.filter(and_(*filters))

            records_filtered = query.count()
            rows = query.offset(start).limit(length).all()

            # Convert rows to dict
            data = [model_to_dict(r,backrefs = True) for r in rows]

        return jsonify({
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data
        })

    def search_by_columns(self, joins: Optional[List[Any]] = None, **kwargs) -> Optional[List[T]]:
        """
        Search records by exact column matches + optional joins.
        Example: search_by_columns(nome="Test", email="abc@test.com", joins=[OtherModel])
        """
        with Session(engine()) as session:
            query = session.query(self.model)
            
            query = self._apply_joins(query, joins)
            
            filters = [getattr(self.model, key) == value for key, value in kwargs.items()]
            query = query.filter(and_(*filters))
            return query.all()

    def search_single_by_columns(self, joins: Optional[List[Any]] = None, **kwargs) -> Optional[T]:
        """
        Fetch a single record by multiple filters with optional joins.
        Example: search_single_by_columns(nome="Test", joins=[OtherModel])
        """
        with Session(engine()) as session:
            query = session.query(self.model)
            query = self._apply_joins(query, joins)
            filters = [getattr(self.model, key) == value for key, value in kwargs.items()]
            return query.filter(and_(*filters)).first()
