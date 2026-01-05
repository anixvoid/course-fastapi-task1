from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.exceptions import ExpiredAccessTokenException, IncorrectAccessTokenException, IncorrectPasswordExpcetion, ObjectAlreadyExistsException, UserAlreadyExistsException, UserNotFoundException
from src.schemas.users import UserAdd, UserRequestAdd
from src.config import settings
from src.services.base import BaseService


class AuthService(BaseService):
    # Кастомная аутентификация, реализация oauth2 через cookies
    # В oauth2 токен содержится в заголовке Authorization (формат "bearer {token}")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError as ex:
            raise IncorrectAccessTokenException from ex
        except jwt.exceptions.ExpiredSignatureError as ex:
            raise ExpiredAccessTokenException from ex

    async def register_user(
        self,
        data        : UserRequestAdd,
    ):
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email = data.email, hashed_password = hashed_password)

        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

        await self.db.commit()

    async def login_user(
        self,
        data        : UserRequestAdd
    ):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotFoundException 
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordExpcetion

        return AuthService().create_access_token({"user_id": user.id})

    async def logout_user(self, user_id : int):        
        pass
        
    async def get_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)