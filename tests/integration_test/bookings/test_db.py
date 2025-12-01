from datetime import date

from src.utils.db_manager import DBManager
from src.schemas.bookings import BookingAdd, BookingPatch

from tests.conftest import db


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2023, month=12, day=12),
        date_to=date(year=2024, month=1, day=1),
        price=100,
    )

    new_booking = await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert new_booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    updated_price = 200
    updated_date = date(year=2024, month=8, day=25)
    booking_path_data = BookingPatch(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=25),
        date_to=updated_date,
        price=updated_price,
    )
    assert (await db.bookings.edit(booking_path_data, exclude_unset=True, id=booking.id)) == 1

    updated_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert updated_booking

    assert updated_booking.price == updated_price
    assert updated_booking.date_to == updated_date

    assert (await db.bookings.delete_by_id(booking.id)) == 1
    assert not (await db.bookings.get_one_or_none(id=booking.id))
