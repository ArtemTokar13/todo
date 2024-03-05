from fastapi import APIRouter, Response, status, Depends
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from db.db import get_db
from db.models import User
from db import db_qry
from db import alter_data
import auth_tools


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'Todo'

user_router = APIRouter()

DB = Annotated[MongoClient, Depends(get_db)]
Token = Annotated[str, Depends(auth_tools.auth_schema)]

@user_router.post('/token')
def create_token(response: Response, db: DB, form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_tools.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return False
    login_data = dict(email=form_data.username,
                      password=form_data.password)
    token = auth_tools.cerate_access_token(login_data)
    return {'access_token': token}

@user_router.post('/create-user')
def create_user(response: Response, user: User, db: DB):
    user_d = db_qry.user(db, email=user.email)
    if user_d is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'Error': 'User with this email already exists'}
    user.password = auth_tools.hash_password(user.password)
    alter_data.create_user(db, user)
    response.status_code = status.HTTP_201_CREATED
    return True

@user_router.get('/read-users')
def read_tasks(response: Response, db: DB, token: Token):
    request_user = auth_tools.verify_token(db, token)
    if request_user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return False
    user_list = db_qry.users(db)
    response.status_code = status.HTTP_200_OK
    if len(user_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'user_list': user_list}

@user_router.get('/read-user/{id}')
def read_user_by_id(response: Response, id: str, db: DB, token: Token):
    request_user = auth_tools.verify_token(db, token)
    if request_user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return False
    res = db_qry.user(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return res

@user_router.put('/update-user/{id}')
def update_user(response: Response, id: str, user: User, db: DB, token: Token):
    request_user = auth_tools.verify_token(db, token)
    if request_user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return False
    user_d = db_qry.user(db, id=id)
    if user_d['email'] != user.email:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'Error': 'You can not modify email'}
    res = alter_data.update_user(db, id, user)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True

@user_router.delete('/delete-user/{id}')
def delete_user(response: Response, id: str, db: DB, token: Token):
    request_user = auth_tools.verify_token(db, token)
    if request_user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return False
    res = alter_data.delete_user(db, id)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True