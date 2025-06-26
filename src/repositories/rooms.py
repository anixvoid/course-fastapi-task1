from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm  import selectinload, joinedload
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room, RoomWithRels

from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model  = RoomsORM
    schema = Room

    async def get_free_by_description_title_price_date(
        self, 
        hotel_id    : int,        
        date_from   : date,
        date_to     : date,
        description : str | None    = None, 
        title       : str | None    = None, 
        min_price   : int | None    = None, 
        max_price   : int | None    = None        
    ):
        filters = [RoomsORM.id.in_(rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id))]

        if title:
            filters.append(RoomsORM.title.icontains(title))
            
        if description:
            filters.append(RoomsORM.description.icontains(description))

        if min_price:
            filters.append(RoomsORM.price >= min_price)

        if max_price:
            filters.append(RoomsORM.price <= max_price)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(*filters)
        )

        result = await self.session.execute(query)

        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]