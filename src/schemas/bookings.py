from datetime import date, datetime

from pydantic import BaseModel, Field

class BookingAddRequest(BaseModel):
    room_id     : int
    date_from   : date
    date_to     : date    

class BookingAdd(BaseModel):
    create_at   : datetime      = Field(default_factory=datetime.now)
    user_id     : int
    room_id     : int
    date_from   : date
    date_to     : date
    price       : int

class BookingPatchRequest(BaseModel):
    date_from   : date  | None
    date_to     : date  | None
    price       : int   | None

class BookingPatch(BaseModel):
    user_id     : int   | None
    room_id     : int   | None
    date_from   : date  | None
    date_to     : date  | None
    price       : int   | None

class Booking(BookingAdd):
    id          : int
    create_at   : datetime      = Field(default_factory=datetime.now)