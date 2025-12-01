from sqlalchemy import select, insert, delete

from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM


class FacilityRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomFacilityDataMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        current_facilities_ids: list[int] = res.scalars().all()
        facility_ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        facility_ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if facility_ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(facility_ids_to_delete),
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if facility_ids_to_insert:
            insert_m2m_facilities_stmt = insert(self.model).values(
                [
                    {"room_id": room_id, "facility_id": facility_id}
                    for facility_id in facility_ids_to_insert
                ]
            )
            await self.session.execute(insert_m2m_facilities_stmt)
