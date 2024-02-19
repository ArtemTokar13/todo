from fastapi import APIRouter, Response, status, Depends
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing_extensions import Annotated

from db.models import Category
from db.db import get_db
from db import db_qry
from db import alter_data


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'Todo'

category_router = APIRouter()

DB = Annotated[MongoClient, Depends(get_db)]

@category_router.post('/create-category')
def create_category(response: Response, category: Category, db: DB):
    alter_data.create_category(db, category)
    response.status_code = status.HTTP_201_CREATED
    return True

@category_router.get('/read-categories')
def read_categories(response: Response, db: DB):
    category_list = db_qry.categories(db)
    response.status_code = status.HTTP_200_OK
    if len(category_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'category_list': category_list}

@category_router.get('/read-category/{id}')
def read_category_by_id(response: Response, id: str, db: DB):
    res = db_qry.category(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return res

@category_router.put('/update-category/{id}')
def update_category(response: Response, id: str, category: Category, db: DB):
    res = alter_data.update_category(db, id, category)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True

@category_router.delete('/delete-category/{id}')
def delete_category(response: Response, id: str, db: DB):
    res = alter_data.delete_category(db, id)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True 