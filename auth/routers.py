from auth.dependencies import (
    ValidateRefreshTokenBearer,
    RoleTokenBearer
)


from fastapi import APIRouter, status, Depends
from db.models import User, UserCreate, UserLogin
from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_engine import get_session
from auth.service import UserService
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from auth.utils import verify_password, create_access_token
from pprint import pprint



auth_router = APIRouter()


role_checker = Depends(RoleTokenBearer(["admin", "user"]))
user_service = UserService()
# acccess_token_bearer = AccessTokenBearer()


@auth_router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED, description="Crear nuevo usuario")
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user




@auth_router.post("/login", description="Iniciar sesión de usuario")
async def login_users(
    login_data: UserLogin, session: AsyncSession = Depends(get_session)
):
    
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)


    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "role": user.role, "user_id": str(user.user_id)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "role": user.role, "user_id": str(user.user_id)},
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "user_id": str(user.user_id), "role":user.role},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )
            



@auth_router.get("/refresh_token", dependencies=[role_checker], description="Renovar token de acceso usando un token de renovación")
async def get_new_access_token(
    token_details: dict = Depends(ValidateRefreshTokenBearer())
    ):


    
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )


