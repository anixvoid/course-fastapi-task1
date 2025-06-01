from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User

from src.schemas.users import UserWithHashedPassword

class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User


    async def get_user_with_hashed_password(self, email:EmailStr):
        query  = select(self.model).filter_by(email = email)
        result = await self.session.execute(query) 
        if model := result.scalars().one_or_none():
            return UserWithHashedPassword.model_validate(model, from_attributes=True)

        return None