from typing import Annotated

from fastapi import Depends, Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page     : Annotated[int | None, Query(default=1, ge=1)]
    per_page : Annotated[int | None, Query(default=3, ge=1, le=100)]

PaginationDep = Annotated[PaginationParams, Depends()]