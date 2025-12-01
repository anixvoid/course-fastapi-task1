from datetime import date

from sqlalchemy import select

from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.models.hotels import HotelsORM

from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_all(self, location: str, title: str, limit: int = 100, offset: int = 0):
        query = select(HotelsORM)

        if title:
            query = query.filter(HotelsORM.title.icontains(title))
        if location:
            query = query.filter(HotelsORM.location.icontains(location))

        query = query.limit(limit).offset(offset)

        # sprint(query)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_free_by_title_location_date(
        self,
        title: str,
        location: str,
        date_from: date,
        date_to: date,
        limit: int | None = None,
        offset: int | None = None,
    ):
        query_hotels_id = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_for_booking(date_from=date_from, date_to=date_to)))
            .distinct()
        )
        query_filters = [HotelsORM.id.in_(query_hotels_id)]

        if title:
            query_filters.append(HotelsORM.title.icontains(title))

        if location:
            query_filters.append(HotelsORM.location.icontains(location))

        return await self.get(*query_filters, limit=limit, offset=offset)
