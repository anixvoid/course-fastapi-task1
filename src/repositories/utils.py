from datetime import date

from sqlalchemy import select, func

from models.bookings import BookingsORM
from models.rooms import RoomsORM

def rooms_ids_for_booking(
        date_from   : date,
        date_to     : date,
        hotel_id    : int | None    = None
):    
        """
        with rooms_count as (
            select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2025-11-07' and date_to >= '2024-07-01'
            group by room_id
        ),
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id 
        )
        select * from rooms_left_table 
        where rooms_left > 0
        """
                
        rooms_count = (
            select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsORM)
            .filter(
                BookingsORM.date_from <= date_to,
                BookingsORM.date_to   >= date_from
            )
            .group_by(BookingsORM.room_id)
            .cte(name = "rooms_count")
        )
        
        rooms_left_table = (
            select(
                RoomsORM.id.label("room_id"), 
                (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .select_from(RoomsORM)
            .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
            .cte(name = "rooms_left_table")
        )

        rooms_ids_filtered = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0                
            )
        )

        if hotel_id is not None:
            rooms_ids_by_hotel_id = (
                select(RoomsORM.id)
                .select_from(RoomsORM)
                .filter_by(hotel_id = hotel_id)
                .subquery()
            )

            rooms_ids_filtered = rooms_ids_filtered.filter(
                rooms_left_table.c.room_id.in_(rooms_ids_by_hotel_id)
            )

        return rooms_ids_filtered