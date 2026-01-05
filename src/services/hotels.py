from datetime import date

from src.exceptions import HotelNotFoundException, ObjectNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService

class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination,
        title       : str | None,
        location    : str | None,
        date_from   : date,
        date_to     : date,
    ):
        page    = pagination.page or 1
        limit   = pagination.per_page or 100
        offset  = limit * (page - 1)

        return await self.db.hotels.get_free_by_title_location_date(
            title       = title,
            location    = location,
            date_from   = date_from,
            date_to     = date_to,
            limit       = limit,
            offset      = offset,
        )
    
    async def get_hotel(
        self,
        hotel_id    : int
    ):
        return await self.db.hotels.get_one(id=hotel_id)
    
    async def add_hotel(
        self,
        data: HotelAdd
    ):
        res = await self.db.hotels.add(data)
        await self.db.commit()
        return res
    
    async def delete_hotel(
        self,
        hotel_id    : int
    ):
        count = await self.db.hotels.delete_by_id(hotel_id)
        await self.db.commit()
        return count
    
    async def edit_hotel(
        self,
        hotel_id        : int,
        hotel_data      : HotelPatch,
        exclude_unset   : bool = False
    ):
        count = await self.db.hotels.edit_by_id(hotel_data, hotel_id, exclude_unset)
        await self.db.commit()
        return count
    
    async def get_hotel_with_check(self, hotel_id: int) -> None:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException    