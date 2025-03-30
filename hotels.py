from fastapi import APIRouter, Query, Body
from pydantic import BaseModel

hotels = [
    {"id": 1, "title": "Сочи",   "name": "sochi"},
    {"id": 2, "title": "Дубай",  "name": "dubai"},
    {"id": 3, "title": "Шанхай", "name": "shanghai"}
]
router = APIRouter(prefix = "/hotels", tags = ["Отели"])

class Hotel(BaseModel):
    title: str 
    name: str

@router.get("")
def get_hotels(
    hotel_id: int | None = Query(None, description = "Идентификатор"),
    title: str | None = Query(None, description = "Название"),
    name: str | None = Query(None, description = "Псевдоним"),
):

    return [hotel for hotel in hotels if (not hotel_id or hotel["id"] == hotel_id) and (not title or hotel["title"] == title) and (not name or hotel["name"] == name)]

@router.post("")
def create_hotel(hotel: Hotel):
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
    hotel: Hotel
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
    title: str | None = None,
    name: str | None = None
):
    global hotels
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title

            if name:
                hotel["name"] = name

            return {
                "status": "OK", 
                "count": len(hotels)
            }

    return {
        "status": "NOK", 
        "message": "Hotel not found"
    }
    