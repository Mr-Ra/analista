from typing import Any, List

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_engine import get_session
from db.models import User
from auth.service import UserService
from pprint import pprint

# user_service = UserService()


from auth.utils import decode_token


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"This token is invalid or expired",
                    "resolution":"Please get new token"
                }
            )


        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return token_data is not None 

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
    



class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"This token is invalid or expired",
                    "resolution":"Please get new token"
                }
            )



    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        # pprint(token_data)

        return token_data is not None 
    



class ValidateRefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )
        



class ValidateAccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized",
            )
        



async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    
    user_email = token_details["user"]["email"]

    user = await UserService().get_user_by_email(user_email, session)

    return user



class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action"
        )
    



class RoleTokenBearer(TokenBearer):
    def __init__(self, allowed_roles: List[str], auto_error=True):
        super().__init__(auto_error=auto_error)
        self.allowed_roles = allowed_roles

    def verify_token_data(self, token_data: dict):
        user_data = token_data.get("user")
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token does not contain user information",
            )
        
        user_role = user_data.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{user_role}' is not allowed to perform this action",
            )