from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title   : str 
    location: str

class HotelPatch(BaseModel):
    title   : str | None    = None
    location: str | None    = None

class Hotel(HotelAdd):
    id      : int