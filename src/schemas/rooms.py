from pydantic import BaseModel, Field

class RoomAdd(BaseModel):
    hotel_id    : int
    title       : str 
    description : str
    price       : int
    quantity    : int

class RoomPut(BaseModel):
    title       : str 
    description : str
    price       : int
    quantity    : int

class RoomPatch(BaseModel):
    title       : str | None    = Field(None) 
    description : str | None    = Field(None)
    price       : int | None    = Field(None)
    quantity    : int | None    = Field(None)

class Room(RoomAdd):
    id      : int


