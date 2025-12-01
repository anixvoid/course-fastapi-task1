from datetime import date, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import BaseORM


class BookingsORM(BaseORM):
    __tablename__ = "bookings"
    __table_args__ = {"keep_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    create_at: Mapped[datetime | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
