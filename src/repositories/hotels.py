from sqlalchemy import select 

from repositories.base import BaseRepository
from src.models.hotels import HotelsORM

class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(self, location:str, title:str, limit:int = 100, offset:int = 0):
        query = select(HotelsORM)

        if title:
            query = query.filter(HotelsORM.title.icontains(title))
        if location:
            query = query.filter(HotelsORM.location.icontains(location))
            
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        #sprint(query)
        result = await self.session.execute(query)
        return result.scalars().all()