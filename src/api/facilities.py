from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facility()


@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(
        openapi_examples={
            "1": {"summary": "Кондиционер", "value": {"title": "Кондиционер"}},
            "2": {"summary": "Холодильник", "value": {"title": "Холодильник"}},
            "3": {"summary": "WiFi", "value": {"title": "WiFi"}},
        }
    ),
):
    facility = await FacilityService(db).add_facility(facility_data) 
    return {"status": "OK", "data": facility}