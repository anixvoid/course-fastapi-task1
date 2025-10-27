from datetime import date

from src.utils.db_manager   import DBManager
from src.schemas.bookings   import BookingAdd, BookingPatch

from tests.conftest         import db

async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        user_id     = user_id,
        room_id     = room_id,
        date_from   = date(year=2023, month=12, day=12),
        date_to     = date(year=2024, month=1,  day=1),
        price       = 100
    )

    booking_id = (await db.bookings.add(booking_data)).id
    assert len(await db.bookings.get(id=booking_id)) == 1
    
    new_price = 200
    booking_path_data = BookingPatch(price=new_price)
    assert (await db.bookings.edit(booking_path_data, exclude_unset=True,id=booking_id)) == 1
    assert (await db.bookings.get_one_or_none(id=booking_id)).price == new_price
    assert (await db.bookings.delete_by_id(booking_id)) == 1
    
    await db.commit()