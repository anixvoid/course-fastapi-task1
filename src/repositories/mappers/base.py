from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.database import BaseORM

DBModelType = TypeVar("DBModelType",    bound=BaseORM)
SchemaType  = TypeVar("SchemaType",     bound=BaseModel)


class DataMapper:
    db_model: type[BaseORM] 
    schema  : type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data: BaseORM | dict | Row | RowMapping) -> SchemaType:
        """SQLA -> Pydantic"""

        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        """Pydantic -> SQLA"""

        return cls.db_model(**data.model_dump())
