from typing import Annotated
from pydantic import BaseModel

from fastapi import Depends, HTTPException, Query, Depends, Request

from services.auth import AuthService
from utils.db_manager import DBManager
from database import async_session_maker

class PaginationParams(BaseModel):
    page     : Annotated[int | None, Query(default=1,  ge=1)]
    per_page : Annotated[int | None, Query(default=10, ge=1, le=100)]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_user_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail = "Не предоставлен токен доступа")
    
    return token
    
def get_user_id(    
    token: str = Depends(get_user_token),
):    
    data = AuthService().decode_token(token)
    user_id = data.get("user_id")

    return user_id

UserIdDep = Annotated[int, Depends(get_user_id)]

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]