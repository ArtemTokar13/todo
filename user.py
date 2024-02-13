from fastapi import APIRouter, Response, status
from db.models import User
from pymongo import MongoClient
from bson.objectid import ObjectId

DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'Todo'

user_router = APIRouter()


@user_router.post('/create-user')
def create_user(response: Response, user: User):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    user = dict(user)
    db.users.insert_one(user)
    response.status_code = status.HTTP_201_CREATED
    return True

@user_router.get('/read-users')
def read_tasks(response: Response):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    cursor = db.users.find()
    user_list = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        user_list.append(document)
    response.status_code = status.HTTP_200_OK
    if len(user_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'user_list': user_list}

@user_router.get('/read-user/{id}')
def read_user_by_id(response: Response, id: str):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    res = db.users.find_one({'_id': ObjectId(id)})
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    res['_id'] = str(res['_id'])
    response.status_code = status.HTTP_200_OK
    return res