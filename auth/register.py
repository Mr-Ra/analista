# from typing import Annotated
# from datetime import datetime, timedelta, timezone
# import jwt
# from jwt.exceptions import InvalidTokenError
# from dotenv import load_dotenv
# import os
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer

# from passlib.context import CryptContext
# from db.models import *

# from db_interface.db import db_engine
# from sqlmodel import Session


# def register_user(user_payload):
#     session = Session(db_engine)
#     new_user = User(**user_payload.dict())
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
#     return