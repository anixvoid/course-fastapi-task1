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
    date_from   : date  | None  = None
    date_to     : date  | None  = None
    price       : int   | None  = None

class BookingPatch(BaseModel):
    user_id     : int   | None  = None
    room_id     : int   | None  = None
    date_from   : date  | None  = None
    date_to     : date  | None  = None
    price       : int   | None  = None

class Booking(BookingAdd):
    id          : int
    create_at   : datetime      = Field(default_factory=datetime.now)