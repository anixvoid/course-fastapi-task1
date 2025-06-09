from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import func

from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep

from database import async_session_maker, engine, sprint

from src.repositories.hotels import HotelsRepository
#from models.hotels import HotelsORM

router = APIRouter(prefix = "/hotels", tags = ["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title:      str | None      = Query(default=None, description = "Название"),
    location:   str | None      = Query(default=None, description = "Местонахождение")
):
    limit  = pagination.per_page or 100
    offset = pagination.per_page * (pagination.page - 1)
     
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location    = location, 
            title       = title,
            limit       = limit,
            offset      = offset
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id:int):
    async with async_session_maker() as session:
        if res := await HotelsRepository(session).get_one_or_none(id=hotel_id):
            return res
        else:
            raise HTTPException(404, "Запись не найдена")
        

@router.post("")
async def create_hotel(hotel: HotelAdd = Body(openapi_examples={
    "1":{"summary": "Сириус", "value":{
        "title": "Отель Сириус 5 звезд у моря",
        "location": "ул. Моря, д. 2"
    }},
    "2": {"summary":"Пекин", "value":{
        "title": "Отель Пекин 4 звезды",
        "location": "ул. Нанкинская, д. 33"
    }},
    })):
    
    async with async_session_maker() as session:
        res = await HotelsRepository(session).add(hotel)
        await session.commit()

    return {
        "status" : "OK",
        "data"   : res
    }

@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int
):
    async with async_session_maker() as session:
        count = await HotelsRepository(session).delete_by_id(hotel_id)
        if count == 0: raise HTTPException(404, detail="Запись не найдена")
        if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

        await session.commit()      

    return {
        "status" : "OK",
        #"count"  : count
    }

@router.put(
    "/{hotel_id}", 
    summary = "Замена данных об отеле"
)
async def update_hotel(
    hotel_id: int,
    hotel: HotelAdd
):
    async with async_session_maker() as session:
        count = await HotelsRepository(session).edit_by_id(hotel, hotel_id)
        if count == 0: raise HTTPException(404, detail="Запись не найдена")
        if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

        await session.commit()

    return {
        "status" : "OK",
        #"count"  : count
    }

@router.patch("/{hotel_id}", summary = "Модификация данных об отеле")
async def modify_hotel(
    hotel_id: int,
    hotel: HotelPatch,
):
    async with async_session_maker() as session:
        count = await HotelsRepository(session).edit_by_id(hotel, hotel_id, True)
        if count == 0: raise HTTPException(404, detail="Запись не найдена")
        if count >= 2: raise HTTPException(400, detail="Записей больше одной")       

        await session.commit()

    return {
        "status" : "OK",
        #"count"  : count
    }