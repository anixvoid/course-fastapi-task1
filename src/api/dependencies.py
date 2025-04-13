from typing import Annotated
from pydantic import BaseModel

from fastapi import Depends, Query, Depends


class PaginationParams(BaseModel):
    page     : Annotated[int | None, Query(default=1,  ge=1)]
    per_page : Annotated[int | None, Query(default=10, ge=1, le=100)]

PaginationDep = Annotated[PaginationParams, Depends()]