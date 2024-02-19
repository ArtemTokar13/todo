from fastapi import APIRouter, Response, status, Depends
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing_extensions import Annotated

from db.db import get_db
from db.models import User
from db import db_qry
from db import alter_data


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'Todo'

user_router = APIRouter()

DB = Annotated[MongoClient, Depends(get_db)]

@user_router.post('/create-user')
def create_user(response: Response, user: User, db: DB):
    alter_data.create_user(db, user)
    response.status_code = status.HTTP_201_CREATED
    return True

@user_router.get('/read-users')
def read_tasks(response: Response, db: DB):
    user_list = db_qry.users(db)
    response.status_code = status.HTTP_200_OK
    if len(user_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'user_list': user_list}

@user_router.get('/read-user/{id}')
def read_user_by_id(response: Response, id: str, db: DB):
    res = db_qry.user(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return res

@user_router.put('/update-task/{id}')
def update_user(response: Response, id: str, user: User, db: DB):
    res = alter_data.update_user(db, id, user)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True

@user_router.delete('/delete-user/{id}')
def delete_user(response: Response, id: str, db: DB):
    res = alter_data.delete_user(db, id)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True