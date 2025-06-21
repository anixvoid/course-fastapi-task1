from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.api.dependencies import DBDep
from src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomAddRequest,RoomPatchRequest

router = APIRouter(prefix = "/hotels", tags = ["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db              : DBDep,
    hotel_id        : int,
    # title           : str | None        = Query(default=None, description = "Название"),
    # description     : str | None        = Query(default=None, description = "Описание"),
    # min_price       : int | None        = Query(default=None, description = "Минимальная цена"),
    # max_price       : int | None        = Query(default=None, description = "Максимальная цена"),
    date_from       : date              = Query(example="2025-01-01"),
    date_to         : date              = Query(example="2025-01-10")
):
    return await db.rooms.get_by_date(
        hotel_id        = hotel_id,            
        # description     = description, 
        # title           = title,
        # min_price       = min_price,
        # max_price       = max_price,
        date_from       = date_from,
        date_to         = date_to
    )
    
    # return await db.rooms.get(
    #     hotel_id        = hotel_id,            
    #     description     = description, 
    #     title           = title,
    #     min_price       = min_price,
    #     max_price       = max_price,
    # )

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db              : DBDep,
    hotel_id        : int,
    room_id         : int
):
    if res := await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id):
        return res
    else:
        raise HTTPException(404, "Запись не найдена")


@router.post("{hotel_id}/rooms")
async def create_room(
    db              : DBDep,
    hotel_id        : int, 
    room            : RoomAddRequest = Body(openapi_examples={
        "1":{"summary": "Люкс", "value":{
            "title"         : "Люкс",
            "description"   : "Самый комфортный номер",
            "price"         : 10000,
            "quantity"      : 3

        }},
        "2":{"summary": "Стандартный", "value":{
            "title"         : "Стандартный",
            "description"   : "Однокомнатный одноместный",
            "price"         : 4000,
            "quantity"      : 12

        }},
        "3":{"summary": "Двухместный", "value":{
            "title"         : "Двухместный",
            "description"   : "Двухместный с одной кроватью",
            "price"         : 7000,
            "quantity"      : 5

        }},
    })):

    _room = RoomAdd(hotel_id=hotel_id, **room.model_dump())
    
    res = await db.rooms.add(_room)
    await db.commit()

    return {
        "status" : "OK",
        "data"   : res
    }

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db              : DBDep,
    hotel_id        : int,
    room_id         : int
):
    count = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    if count == 0: raise HTTPException(404, detail = "Запись не найдена")
    if count >= 2: raise HTTPException(400, detail = "Записей больше одной")       

    await db.commit()      

    return {
        "status" : "OK",
        #"count"  : count
    }

@router.put(
    "/{hotel_id}/rooms/{room_id}", 
    summary = "Замена данных об отеле"
)
async def update_room(
    db              : DBDep,
    hotel_id        : int,
    room_id         : int,
    room            : RoomAddRequest
):
    _room = RoomAdd(hotel_id=hotel_id, **room.model_dump())
    count = await db.rooms.edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if count == 0: raise HTTPException(404, detail = "Запись не найдена")
    if count >= 2: raise HTTPException(400, detail = "Записей больше одной")       

    await db.commit()

    return {
        "status" : "OK"
    }

@router.patch("/{hotel_id}/rooms/{room_id}", summary = "Модификация данных о комнате")
async def edit_room(
    db              : DBDep,
    hotel_id        : int,
    room_id         : int,
    room            : RoomPatchRequest,
):
    _room = RoomPatch(hotel_id=hotel_id, **room.model_dump(exclude_unset=True))
    count = await db.rooms.edit(_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if count == 0: raise HTTPException(404, detail="Запись не найдена")
    if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

    await db.commit()

    return {
        "status" : "OK"
    }