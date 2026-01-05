from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.rooms import Room
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService

class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get()

    async def get_booking(self, user_id: int):
        return await self.db.bookings.get(user_id=user_id) # type: ignore

    async def add_booking(
        self,
        user_id: int,
        booking_data: BookingAddRequest,
    ):
        try:
            room : Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        room_price = room.price

        _booking_data = BookingAdd(
            user_id = user_id, 
            price   = room_price, 
            **booking_data.model_dump()
        )

        booking = await self.db.bookings.add_booking(_booking_data)
        await self.db.commit()

        return booking