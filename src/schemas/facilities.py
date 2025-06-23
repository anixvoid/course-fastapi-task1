from pydantic import BaseModel

class FacilityAdd(BaseModel):
    title       : str

class FacilityPatch(BaseModel):
    title       : str   | None

class Facility(FacilityAdd):
    id          : int