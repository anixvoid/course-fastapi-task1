from datetime import date

from src.services.base import BaseService

class FacilityService(BaseService):
    async def get_facility(self):
        return await self.db.facilities.get_all()
    
    async def add_facility(self, facility_data):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        return facility
