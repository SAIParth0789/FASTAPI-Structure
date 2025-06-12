import logging
from builtins import str
from enum import Enum
import sqlalchemy
from fastapi import Depends, APIRouter, HTTPException, status
from typing import List

# models imports
from project_name.models.user import AdminUserIn

#database imports
from project_name.database import admin_user_table, database

from project_name.security import (
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    # get_subject_for_token_type,
    # create_confirmation_token
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/admin_register", status_code=201)
async def register(user: AdminUserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists"
        )
    hashed_password = get_password_hash(user.password)
    query = admin_user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)
    await database.execute(query)
    return {"detail": "User created."}


# ---------------- For get JSON Data in the Body --------------------
# @router.post("/admin_token", status_code=status.HTTP_200_OK)
# async def login(user: AdminUserIn):
#     user = await authenticate_user(user.email, user.password)
#     access_token = create_access_token(user.email)
#     return {"access_token": access_token, "token_type": "bearer"}


# --------------- For Form Data and Swagger Auth Testing ---------------
from fastapi.security import OAuth2PasswordRequestForm
@router.post("/admin_token", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}