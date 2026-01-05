from datetime import date

from src.services.hotels import HotelService
from src.exceptions import HotelNotFoundException, ObjectNotFoundException, RoomNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.services.base import BaseService

class RoomService(BaseService):
    async def get_rooms(
        self,
        hotel_id: int,
        title: str | None,
        description: str | None,
        min_price: int | None,
        max_price: int | None,
        date_from: date,
        date_to: date,
    ):
        return await self.db.rooms.get_free_by_description_title_price_date(
            hotel_id=hotel_id,
            description=description,
            title=title,
            min_price=min_price,
            max_price=max_price,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_room(
            self, 
            hotel_id: int, 
            room_id: int
    ):
        return await self.db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)

    async def add_room(
        self,
        hotel_id: int,
        room_data: RoomAddRequest 
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
            for facility_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

        return room

    async def delete_room(
            self, 
            hotel_id: int, 
            room_id: int
        ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        count = await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

        return count

    async def update_room(
            self, 
            hotel_id: int, 
            room_id: int, 
            room_data: RoomAddRequest
        ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        count = await self.db.rooms.edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)

        await self.db.rooms_facilities.set_room_facilities(room_id, room_data.facilities_ids)
        await self.db.commit()

        return count

    async def edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        count = 0
        if len(_room_data.model_dump(exclude_unset=True)):
            count = await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

        if room_data.facilities_ids is not None:
            await self.db.rooms_facilities.set_room_facilities(room_id, room_data.facilities_ids)

        await self.db.commit()

        return count
    
    async def get_room_with_check(self, room_id: int) -> None:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException