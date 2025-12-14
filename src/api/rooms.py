# ruff: noqa: E701

from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.exceptions import ObjectNotFoundException, ValidationException
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
        return await db.rooms.get_free_by_description_title_price_date(
            hotel_id=hotel_id,
            description=description,
            title=title,
            min_price=min_price,
            max_price=max_price,
            date_from=date_from,
            date_to=date_to,
        )
    except ValidationException as ex:
        ...


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Номер не найден")

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
        hotel = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(422, "Отель не найден")

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
        for facility_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Номер не найден")

    count = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    if count == 0:
        raise HTTPException(404, detail="Запись не найдена")
    if count >= 2:
        raise HTTPException(400, detail="Записей больше одной")

    await db.commit()

    return {
        "status": "OK",
        # "count"  : count
    }


@router.put("/{hotel_id}/rooms/{room_id}", summary="Замена данных об отеле")
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Номер не найден")

    _room = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    count = await db.rooms.edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if count == 0:
        raise HTTPException(404, detail="Запись не найдена")
    if count >= 2:
        raise HTTPException(400, detail="Записей больше одной")

    await db.rooms_facilities.set_room_facilities(room_id, room_data.facilities_ids)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Модификация данных о комнате")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, "Комната не найдена")

    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    if len(_room_data.model_dump(exclude_unset=True)):
        count = await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if count == 0:
            raise HTTPException(404, detail="Запись не найдена")
        if count >= 2:
            raise HTTPException(400, detail="Записей больше одной")

    if room_data.facilities_ids is not None:
        await db.rooms_facilities.set_room_facilities(room_id, room_data.facilities_ids)

    await db.commit()

    return {"status": "OK"}