from datetime import date

from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room

from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model  = RoomsORM
    schema = Room

    async def get_all(self, hotel_id: int, description:str, title:str, min_price: int = 0, max_price: int = 0):
        query = select(RoomsORM).filter_by(hotel_id=hotel_id)

        if title:
            query = query.filter(RoomsORM.title.icontains(title))
            
        if description:
            query = query.filter(RoomsORM.description.icontains(description))

        if min_price:
            query = query.filter(RoomsORM.price >= min_price)

        if max_price:
            query = query.filter(RoomsORM.price <= max_price)

        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    
    async def get_by_date(
        self, 
        hotel_id    : int,
        date_from   : date,
        date_to     : date
    ):
        return await self.get(RoomsORM.id.in_(rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)))