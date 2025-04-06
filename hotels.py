from fastapi import APIRouter, Query, Body
from schemas.hotels import HotelSchema, HotelPATCH
from dependencies import PaginationDep

hotels = [
    {"id": 1, "title": "Сочи",              "name": "sochi"},
    {"id": 2, "title": "Дубай",             "name": "dubai"},
    {"id": 3, "title": "Шанхай",            "name": "shanghai"},
    {"id": 4, "title": "Геленджик",         "name": "gelendzhik"},
    {"id": 5, "title": "Москва",            "name": "moscow"},
    {"id": 6, "title": "Казанть",           "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург",   "name": "spb"},
]
router = APIRouter(prefix = "/hotels", tags = ["Отели"])

@router.get("")
def get_hotels(
    pagination: PaginationDep,
    hotel_id: int | None = Query(default=None, description = "Идентификатор"),
    title: str | None    = Query(default=None, description = "Название"),
    name: str | None     = Query(default=None, description = "Псевдоним"),
    #page: int | None     = Query(default=1, gt=1),
    #per_page: int | None = Query(default=3, gt=1, lt=100),
):
    return [hotel for hotel in hotels if (not hotel_id or hotel["id"] == hotel_id) and (not title or hotel["title"] == title) and (not name or hotel["name"] == name)][(page-1)*(per_page):page*per_page]

@router.post("")
def create_hotel(hotel: HotelSchema = Body(openapi_examples={
    "1":{"summary": "Сириус", "value":{
        "title": "Отель Сириус 5 звезд у моря",
        "name": "sirius"
    }},
    "2": {"summary":"Пекин", "value":{
        "title": "Отель Пекин 4 звезды",
        "name": "pekin"
    }},
    })):
    global hotels

    hotel = {
        "id"    : hotels[-1]["id"] + 1,
        "title" : hotel.title,
        "name"  : hotel.name,
    }
    hotels.append(hotel)

    return {
        "status" : "OK",
        "id"     : hotel["id"]
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
    