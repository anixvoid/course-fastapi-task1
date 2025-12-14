from fastapi import APIRouter, Body, HTTPException

from src.exceptions import NoRoomsAvailableException, ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.rooms import Room
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get()


@router.get("/me")
async def get_booking_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get(user_id=user_id) # type: ignore


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Новогодние каникулы",
                "value": {
                    "room_id": 3,
                    "date_from": "2025-01-01",
                    "date_to": "2025-01-10",
                },
            },
            "2": {
                "summary": "Командировка",
                "value": {
                    "room_id": 5,
                    "date_from": "2025-03-01",
                    "date_to": "2025-03-07",
                },
            },
        }
    ),
):
    #if not (room := await db.rooms.get_one_or_none(id=booking_data.room_id)):
        #raise HTTPException(404, detail="Room not found")

    try:
        room : Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex

    room_price = room.price

    _booking_data = BookingAdd(
        user_id=user_id, 
        price=room_price, 
        **booking_data.model_dump()
    )

    try:
        booking = await db.bookings.add_booking(_booking_data)
    except NoRoomsAvailableException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()

    return {"status": "OK", "data": booking}