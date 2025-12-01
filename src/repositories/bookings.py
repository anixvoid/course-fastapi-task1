from datetime import date
from fastapi import HTTPException
from sqlalchemy import select

from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsORM).filter(BookingsORM.date_from == date.today())

        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking: BookingAdd):
        free_room_ids = (
            (
                await self.session.execute(
                    rooms_ids_for_booking(date_from=booking.date_from, date_to=booking.date_to)
                )
            )
            .unique()
            .scalars()
            .all()
        )

        if booking.room_id not in free_room_ids:
            raise HTTPException(500, "Missing free rooms")

        return await self.add(booking)
