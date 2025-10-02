import json

from fastapi import APIRouter, Query, Body
from fastapi.exceptions import HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import Facility, FacilityAdd, FacilityPatch

from src.init import redis_manager

router = APIRouter(prefix = "/facilities", tags = ["Удобства"])

@router.get("")
async def get_facilities(db: DBDep):
    FACILITIES_CACHE_KEY = "/cache/facilities"

    facilities_from_cache = await redis_manager.get(FACILITIES_CACHE_KEY)

    if not facilities_from_cache:   
        facilities = await db.facilities.get_all()
        facilities_schemas = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)        
        await redis_manager.set(FACILITIES_CACHE_KEY, facilities_json)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts

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