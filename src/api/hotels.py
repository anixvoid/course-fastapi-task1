# ruff: noqa: E701

from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import HotelNotFoundHTTPException, ValidationException
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch
from src.exceptions import ObjectNotFoundException

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название"),
    location: str | None = Query(default=None, description="Местонахождение"),
    date_from: date = Query(example="2025-01-01"),
    date_to: date = Query(example="2025-01-10"),
):
    """Получение свободных отелей"""

    page  = pagination.page or 1
    limit = pagination.per_page or 100
    offset = limit * (page - 1)

    try:
        return await db.hotels.get_free_by_title_location_date(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
    except ValidationException as ex:
        raise HTTPException(422, detail=ex.detail) from ex


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сириус",
                "value": {
                    "title": "Отель Сириус 5 звезд у моря",
                    "location": "ул. Моря, д. 2",
                },
            },
            "2": {
                "summary": "Пекин",
                "value": {
                    "title": "Отель Пекин 4 звезды",
                    "location": "ул. Нанкинская, д. 33",
                },
            },
        }
    ),
):
    res = await db.hotels.add(hotel)
    await db.commit()

    return {"status": "OK", "data": res}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    count = await db.hotels.delete_by_id(hotel_id)
    if count == 0:
        raise HTTPException(404, detail="Запись не найдена")
    if count >= 2:
        raise HTTPException(400, detail="Записей больше одной")

    await db.commit()

    return {
        "status": "OK",
        # "count"  : count
    }


@router.put("/{hotel_id}", summary="Замена данных об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel: HotelAdd):
    count = await db.hotels.edit_by_id(hotel, hotel_id)
    if count == 0:
        raise HTTPException(404, detail="Запись не найдена")
    if count >= 2:
        raise HTTPException(400, detail="Записей больше одной")

    await db.commit()

    return {
        "status": "OK",
        # "count"  : count
    }


@router.patch("/{hotel_id}", summary="Модификация данных об отеле")
async def modify_hotel(
    db: DBDep,
    hotel_id: int,
    hotel: HotelPatch,
):
    count = await db.hotels.edit_by_id(hotel, hotel_id, True)
    if count == 0:
        raise HTTPException(404, detail="Запись не найдена")
    if count >= 2:
        raise HTTPException(400, detail="Записей больше одной")

    await db.commit()

    return {
        "status": "OK",
        # "count"  : count
    }
