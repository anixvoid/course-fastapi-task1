from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import func

from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep

from database import async_session_maker, engine, sprint

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomPut

router = APIRouter(prefix = "/hotels", tags = ["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id        : int,
    title           : str | None      = Query(default=None, description = "Название"),
    description     : str | None      = Query(default=None, description = "Описание"),
    min_price       : int | None      = Query(default=None, description = "Минимальная цена"),
    max_price       : int | None      = Query(default=None, description = "Максимальная цена"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id        = hotel_id,            
            description     = description, 
            title           = title,
            min_price       = min_price,
            max_price       = max_price,
        )

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id : int,
    room_id  : int
):
    async with async_session_maker() as session:
        if res := await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id):
            return res
        else:
            raise HTTPException(404, "Запись не найдена")


@router.post("{hotel_id}/rooms")
async def create_room(room: RoomAdd = Body(openapi_examples={
    "1":{"summary": "Люкс", "value":{
        "hotel_id"      : 1,
        "title"         : "Люкс",
        "description"   : "Самый комфортный номер",
        "price"         : 10000,
        "quantity"      : 3

    }},
    "2":{"summary": "Стандартный", "value":{
        "hotel_id"      : 1,
        "title"         : "Стандартный",
        "description"   : "Однокомнатный одноместный",
        "price"         : 4000,
        "quantity"      : 12

    }},
    "3":{"summary": "Двухместный", "value":{
        "hotel_id"      : 2,
        "title"         : "Двухместный",
        "description"   : "Двухместный с одной кроватью",
        "price"         : 7000,
        "quantity"      : 5

    }},
    })):
    
    async with async_session_maker() as session:
        res = await RoomsRepository(session).add(room)
        await session.commit()

    return {
        "status" : "OK",
        "data"   : res
    }

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        count = await RoomsRepository(session).delete_by_id(room_id)
        if count == 0: raise HTTPException(404, detail="Запись не найдена")
        if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

        await session.commit()      

    return {
        "status" : "OK",
        #"count"  : count
    }

@router.put(
    "/{hotel_id}/rooms/{room_id}", 
    summary = "Замена данных об отеле"
)
async def update_room(
    hotel_id : int,
    room_id  : int,
    room     : RoomPut
):
    async with async_session_maker() as session:
        count = await RoomsRepository(session).edit_by_id(room, room_id)
        if count == 0: raise HTTPException(404, detail="Запись не найдена")
        if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

        await session.commit()

    return {
        "status" : "OK"
    }

@router.patch("/{hotel_id}/rooms/{room_id}", summary = "Модификация данных о комнате")
async def modify_room(
    hotel_id: int,
    room_id: int,
    room: RoomPatch,
):
    async with async_session_maker() as session:
        count = await RoomsRepository(session).edit_by_id(room, room_id, True)
        if count == 0: raise HTTPException(404, detail="Запись не найдена")
        if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

        await session.commit()

    return {
        "status" : "OK"
    }