from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import Facility, FacilityAdd, FacilityPatch

router = APIRouter(prefix = "/facilities", tags = ["Удобства"])

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get()

@router.post("")
async def create_facility(
    db              : DBDep, 
    facility_data   : FacilityAdd = Body(openapi_examples={
    "1":{"summary": "Кондиционер", "value":{
        "title": "Кондиционер"
    }},
    "2": {"summary":"Холодильник", "value":{
        "title": "Холодильник"
    }},
    "3": {"summary":"WiFi", "value":{
        "title": "WiFi"
    }},
})):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {
        "status" : "OK",
        "data"   : facility
    }