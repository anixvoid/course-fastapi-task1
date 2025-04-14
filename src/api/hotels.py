from fastapi import APIRouter, Query, Body
from src.schemas.hotels import HotelSchema, HotelPATCH
from src.api.dependencies import PaginationDep
from sqlalchemy import insert
from sqlalchemy import select

from database import async_session_maker, engine
from models.hotels import HotelsORM

# hotels = [
#     {"id": 1, "title": "Сочи",              "name": "sochi"},
#     {"id": 2, "title": "Дубай",             "name": "dubai"},
#     {"id": 3, "title": "Шанхай",            "name": "shanghai"},
#     {"id": 4, "title": "Геленджик",         "name": "gelendzhik"},
#     {"id": 5, "title": "Москва",            "name": "moscow"},
#     {"id": 6, "title": "Казанть",           "name": "kazan"},
#     {"id": 7, "title": "Санкт-Петербург",   "name": "spb"},
# ]
router = APIRouter(prefix = "/hotels", tags = ["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    hotel_id:   int | None      = Query(default=None, description = "Идентификатор"),
    title:      str | None      = Query(default=None, description = "Название"),
    location:   str | None      = Query(default=None, description = "Местонахождение")
):
    query = select(HotelsORM)
    if hotel_id:
        query = query.filter_by(id=hotel_id)
    if title:
        query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
    if location:
        query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
    query = (
        query
        .limit(pagination.per_page)
        .offset(pagination.per_page * (pagination.page - 1))
    )

    async with async_session_maker() as session:
        result = await session.execute(query)
        return result.scalars().all()


@router.post("")
async def create_hotel(hotel: HotelSchema = Body(openapi_examples={
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
        stmt_insert = insert(HotelsORM).values(**hotel.model_dump())
        #print(stmt_insert)
        #print(stmt_insert.compile(engine, compile_kwargs={"literal_binds": True})) # Формирование RAW SQL запроса 
        await session.execute(stmt_insert)
        await session.commit()

    return {
        "status" : "OK",
        #"id"     : hotel["id"]
    }

@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int
):
    global hotels
    hotels = list([hotel for hotel in hotels if hotel["id"] != hotel_id])
    return {
        "status" : "OK", 
        "count"   : len(hotels)
    }

@router.put("/{hotel_id}", summary = "Замена данных об отеле")
def update_hotel(
    hotel_id: int,
    hotel: HotelSchema
):
    global hotels
    for i, h in enumerate(hotels):
        if h["id"] == hotel_id:
            hotels[i] = {
                "id":    hotel_id, 
                "title": hotel.title,
                "name":  hotel.name
            }

            return {
                "status": "OK", 
                "count":  len(hotels)
            }

    return {
        "status":  "NOK", 
        "message": "Hotel not found"
    }

@router.patch("/{hotel_id}", summary = "Модификация данных об отеле")
def modify_hotel(
    hotel_id: int,
    hotel: HotelPATCH,
):
    global hotels
    for i, h  in enumerate(hotels):
        if h["id"] == hotel_id:
            if hotel.title:
                h["title"] = hotel.title

            if hotel.name:
                h["name"] = hotel.name

            return {
                "status": "OK", 
                "count": len(hotels)
            }

    return {
        "status": "NOK", 
        "message": "Hotel not found"
    }
    