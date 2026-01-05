from fastapi import APIRouter, Response

from src.exceptions import IncorrectPasswordExpcetion, IncorrectPasswordHTTPExpcetion, UserNotFoundHTTPException, UserAlreadyExistsException, UserAlreadyExistsHTTPException, UserNotFoundException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UserRequestAdd, UserAdd

from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация аутентификация"])

@router.post("/register")
async def register_user(
    db          : DBDep,
    data        : UserRequestAdd,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException as ex:
        raise UserAlreadyExistsHTTPException from ex

@router.post("/login")
async def login_user(
    db          : DBDep,
    data        : UserRequestAdd,
    response    : Response
):
    access_token = None

    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    except IncorrectPasswordExpcetion as ex:
        raise IncorrectPasswordHTTPExpcetion from ex

    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}
    
@router.post("/logout")
async def logout_user(
    user_id     : UserIdDep, 
    response    : Response):        
    response.delete_cookie("access_token")
    
    return {"status": "OK"}
    
@router.get("/me")
async def get_me(
    db          : DBDep,
    user_id     : UserIdDep
):
    return await AuthService(db).get_user(user_id)