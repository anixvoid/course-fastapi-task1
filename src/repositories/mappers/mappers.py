from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facility, RoomFacility
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.schemas.bookings import Booking
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User, UserWithHashedPassword
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel
from src.repositories.mappers.base import DataMapper

class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema   = User

class UserDataWithHashedPasswordMapper(DataMapper):
    db_model = UsersORM
    schema   = UserWithHashedPassword

class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema   = Hotel

class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema   = Room

class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema   = RoomWithRels

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema   = Facility

class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema   = RoomFacility

class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema   = Booking