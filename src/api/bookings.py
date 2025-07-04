from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest, BookingPatch, BookingPatchRequest

router = APIRouter(prefix = "/bookings", tags = ["Бронирования"])

@router.get("")
async def get_bookings(db: DBDep):
    return await db.booking.get()

@router.get("/me")
async def get_booking_me(db: DBDep, user_id: UserIdDep):
    return await db.booking.get(user_id=user_id)

@router.post("")
async def create_booking(
    db              : DBDep, 
    user_id         : UserIdDep,
    booking_data    : BookingAddRequest = Body(openapi_examples={
        "1":{"summary"  : "Новогодние каникулы", "value":{
            "room_id"   : 3,
            "date_from" : "2025-01-01",
            "date_to"   : "2025-01-10"
        }},
        "2": {"summary":"Командировка", "value":{
            "room_id"   : 5,
            "date_from" : "2025-03-01",
            "date_to"   : "2025-03-07"
        }},
    })):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    
    _booking_data = BookingAdd(user_id = user_id, price = room_price, **booking_data.model_dump())

    booking = await db.booking.add(_booking_data)
    await db.commit()

    return {
        "status" : "OK",
        "data"   : booking
    }