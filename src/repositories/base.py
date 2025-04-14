from sqlalchemy import select, insert
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
    
    async def add(self, **data):
        stmt = insert(self.model).values(**data).returning(self.model)
        #sprint(stmt)

        res  = await self.session.execute(stmt)
        return res.scalars().one_or_none()