from typing import Any

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from src.repositories.mappers.base import DataMapper

from src.database import sprint

class BaseRepository:
    model               = None
    schema: BaseModel   = None
    mapper: DataMapper  = None

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by)  -> BaseModel | None:
        query  = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query) 
        if model := result.scalars().one_or_none():
            return self.mapper.map_to_domain_entity(model)

        return None

    async def get(self, *filter: list[Any], limit: int = None, offset: int = None, **filter_by: dict[Any]) -> list[BaseModel]:
        query  = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )

        if limit is not None:
            query = query.limit(limit)

        if offset is not None:
            query = query.offset(offset)

        result = await self.session.execute(query) 
        if models := result.scalars().all():
            return [self.mapper.map_to_domain_entity(model) for model in models]

    async def add(self, data: BaseModel):
        
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        #sprint(stmt)

        res = await self.session.execute(stmt)
        if model := res.scalars().one():     
            return self.mapper.map_to_domain_entity(model)    

    async def add_bulk(self, items: list[BaseModel]):
        if items:
            stmt = insert(self.model).values([item.model_dump() for item in items])
            #sprint(stmt)

            await self.session.execute(stmt)
    
    async def edit(self, data:BaseModel, exclude_unset: bool = False, **filter_by) -> int: #возврат количества
        stmt = update(self.model).values(**data.model_dump(exclude_unset=exclude_unset)).filter_by(**filter_by)
        #sprint(stmt)

        res  = await self.session.execute(stmt)
        return res.rowcount

    async def edit_by_id(self, data:BaseModel, id:int, exclude_unset: bool = False) -> int: #возврат количества
        return await self.edit(data, exclude_unset, id=id)

    async def delete(self, *filter, **filter_by) -> int: #возврат количества
        stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
        #sprint(stmt)

        res  = await self.session.execute(stmt)
        return res.rowcount

    async def delete_by_id(self, id:int) -> int: #возврат количества
        return await self.delete(id=id)
    
    async def delete_by_ids(self, ids: list[int]) -> int: #возврат количества
        if ids:
            return await self.delete(self.model.id.in_(ids))