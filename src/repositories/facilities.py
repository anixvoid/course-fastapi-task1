from repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facility, RoomFacility

class FacilityRepository(BaseRepository):
    model  = FacilitiesORM
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model  = RoomsFacilitiesORM
    schema = RoomFacility
