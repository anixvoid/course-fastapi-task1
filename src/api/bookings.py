from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException
from src.api.dependencies import DBDep, UserIdDep
from schemas.bookings import Booking, BookingAdd, BookingAddRequest, BookingPatch, BookingPatchRequest

router = APIRouter(prefix = "/bookings", tags = ["Бронирования"])

@router.post("")
async def create_booking(
    db          : DBDep, 
    user_id     : UserIdDep,
    room_id     : int,
    booking     : BookingAddRequest = Body(openapi_examples={
        "1":{"summary"  : "Новогодние каникулы", "value":{
            "date_from" : "2025-01-01",
            "date_to"   : "2025-01-10",
            "price"     : 7000
        }},
        "2": {"summary":"Командировка", "value":{
            "date_from" : "2025-03-01",
            "date_to"   : "2025-03-07",
            "price"     : 5000
        }},
    })):
    _booking = BookingAdd(user_id = user_id, room_id = room_id, **booking.model_dump())

    res = await db.booking.add(_booking)
    await db.commit()

    return {
        "status" : "OK",
        "data"   : res
    }
