from pydantic import BaseModel

from sqlalchemy import select, insert, delete, update
from database import sprint

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query  = select(self.model)
        result = await self.session.execute(query) 
        
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query  = select(self.model).fileter_by(**filter_by)
        result = await self.session.execute(query) 
        
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        #sprint(stmt)

        res  = await self.session.execute(stmt)
        return res.scalars().one()   
    
    async def edit(self, data:BaseModel, **filter_by) -> int: #возврат количества
        stmt = update(self.model).values(**data.model_dump()).filter_by(**filter_by)
        #sprint(stmt)

        res  = await self.session.execute(stmt)
        return res.rowcount

    async def edit_by_id(self, data:BaseModel, id:int) -> int: #возврат количества
        return await self.edit(data, id=id)

    async def delete(self, **filter_by) -> int: #возврат количества
        stmt = delete(self.model).filter_by(**filter_by)
        #sprint(stmt)

        res  = await self.session.execute(stmt)
        return res.rowcount

    async def delete_by_id(self, id:int) -> int: #возврат количества
        return await self.delete(id=id)


    # async def add(self, **data):
    #     stmt = insert(self.model).values(**data).returning(self.model)
    #     #sprint(stmt)

    #     res  = await self.session.execute(stmt)
    #     return res.scalars().one_or_none()