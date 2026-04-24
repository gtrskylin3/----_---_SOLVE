import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
)
from fastapi_users.authentication.strategy import JWTStrategy

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users import FastAPIUsers

from app.database.models.users import User
from app.database.session import get_async_session
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession # Added this import

SECRET = settings.SECRET_KEY

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

cookie_transport = CookieTransport(cookie_name="fipi_cookie", cookie_max_age=604800*6, cookie_samesite='none') # 7 days

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=604800*6) # 7 days

auth_backend = AuthenticationBackend(
    name="jwt", # Use "jwt" as the name for the strategy
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True, optional=True)
current_required_user = fastapi_users.current_user(active=True)