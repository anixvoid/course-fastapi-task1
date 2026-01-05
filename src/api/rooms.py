# ruff: noqa: E701

from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.services.rooms import RoomService
from src.exceptions import HotelNotFoundException, HotelNotFoundHTTPException, ObjectNotFoundException, RoomNotFoundException, RoomNotFoundHTTPException, ValidationException
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.schemas.facilities import RoomFacilityAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    title: str | None = Query(default=None, description="Название"),
    description: str | None = Query(default=None, description="Описание"),
    min_price: int | None = Query(default=None, description="Минимальная цена"),
    max_price: int | None = Query(default=None, description="Максимальная цена"),
    date_from: date = Query(example="2025-01-01"),
    date_to: date = Query(example="2025-01-10"),
):
    """Получение свободных комнат отеля"""

    try:
        return await RoomService(db).get_rooms(
            hotel_id=hotel_id,
            description=description,
            title=title,
            min_price=min_price,
            max_price=max_price,
            date_from=date_from,
            date_to=date_to,
        )
    except ValidationException as ex:
        raise HTTPException(422, detail=ex.detail) from ex


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex

@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс",
                    "description": "Самый комфортный номер",
                    "price": 10000,
                    "quantity": 3,
                    "facilities_ids": [1, 2, 3],
                },
            },
            "2": {
                "summary": "Стандартный",
                "value": {
                    "title": "Стандартный",
                    "description": "Однокомнатный одноместный",
                    "price": 4000,
                    "quantity": 12,
                    "facilities_ids": [2, 3, 4],
                },
            },
            "3": {
                "summary": "Двухместный",
                "value": {
                    "title": "Двухместный",
                    "description": "Двухместный с одной кроватью",
                    "price": 7000,
                    "quantity": 5,
                    "facilities_ids": [3, 4, 5],
                },
            },
        }
    ),
):
    try:
        return await RoomService(db).add_room(hotel_id, room_data)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        count = await RoomService(db).delete_room(hotel_id = hotel_id, room_id=room_id)
        if count == 0:
            raise HTTPException(404, detail="Запись не найдена")
        if count >= 2:
            raise HTTPException(400, detail="Записей больше одной")
    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex

    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Замена данных об отеле")
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        count = await RoomService(db).update_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
        if count == 0:
            raise HTTPException(404, detail="Запись не найдена")
        if count >= 2:
            raise HTTPException(400, detail="Записей больше одной")

    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Модификация данных о комнате")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    try:
        count = await RoomService(db).update_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
        if count == 0:
            raise HTTPException(404, detail="Запись не найдена")
        if count >= 2:
            raise HTTPException(400, detail="Записей больше одной")

    except ObjectNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex

    return {"status": "OK"}