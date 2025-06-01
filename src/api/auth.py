from fastapi import APIRouter, HTTPException, Response, Request
from sqlalchemy.exc import IntegrityError

from api.dependencies import UserIdDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository

from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация аутентификация"])

@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except IntegrityError as e:
            raise HTTPException(422, "Не корректные входные данные")

        await session.commit()

    return {"status": "OK"}

@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401  , detail="Пароль не верный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return {"access_token": access_token}
    
@router.post("/logout")
async def logout_user(user_id: UserIdDep, response: Response):        
    response.delete_cookie("access_token")
    
    return {"status": "OK"}
    
@router.get("/me")
async def get_me(
    user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user    