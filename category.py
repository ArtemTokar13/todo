from fastapi import APIRouter, Response, status
from db.models import Category
from pymongo import MongoClient
from bson.objectid import ObjectId

DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'Todo'

category_router = APIRouter()


@category_router.post('/create-category')
def create_category(response: Response, category: Category):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    category = dict(category)
    db.categories.insert_one(category)
    response.status_code = status.HTTP_201_CREATED
    return True

@category_router.get('/read-categories')
def read_categories(response: Response):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    cursor = db.categories.find()
    category_list = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        category_list.append(document)
    response.status_code = status.HTTP_200_OK
    if len(category_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'category_list': category_list}

@category_router.get('/read-category/{id}')
def read_category_by_id(response: Response, id: str):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    res = db.categories.find_one({'_id': ObjectId(id)})
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    res['_id'] = str(res['_id'])
    response.status_code = status.HTTP_200_OK
    return res