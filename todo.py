from fastapi import APIRouter, Response, status, Depends
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing_extensions import Annotated

from db.db import get_db
from db.models import Task
from db import db_qry
from db import alter_data
import auth_tools


todo_router = APIRouter()

DB = Annotated[MongoClient, Depends(get_db)]
Token = Annotated[str, Depends(auth_tools.validate_token)]

@todo_router.get('/read-tasks')
def read_tasks(response: Response, db: DB, token: Token):
    todo_list = db_qry.todos(db)
    response.status_code = status.HTTP_200_OK
    if len(todo_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'todo_list': todo_list}

@todo_router.get('/read-task/{id}')
def read_task_by_id(response: Response, id: str, db: DB):
    res = db_qry.todo(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return res

@todo_router.post('/create-task')
def create_task(response: Response, task: Task, db: DB):
    alter_data.create_task(db, task)
    response.status_code = status.HTTP_201_CREATED
    return True

@todo_router.put('/update-task/{id}')
def update_task(response: Response, id: str, task: Task, db: DB):
    res = alter_data.update_task(db, id, task)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True

@todo_router.put('/update-status/{id}')
def update_status(response: Response, id: str, db: DB):
    res = db_qry.todo(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    alter_data.update_status(db, id, res['is_active'])
    response.status_code = status.HTTP_200_OK
    return True


@todo_router.delete('/delete-task/{id}')
def delete_task(response: Response, id: str, db: DB):
    res = alter_data.delete_task(db, id)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True
    

