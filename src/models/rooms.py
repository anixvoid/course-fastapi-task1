from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM

class RoomsORM(BaseORM):
    __tablename__   = "rooms"
    __table_args__  = {"keep_existing": True}

    id          : Mapped[int] = mapped_column(primary_key=True)
    hotel_id    : Mapped[int] = mapped_column(ForeignKey("hotels.id"))

    title       : Mapped[str]
    description : Mapped[str | None]

    price       : Mapped[int]
    quantity    : Mapped[int]