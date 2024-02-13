from fastapi import APIRouter, Response, status, Depends
from pymongo import MongoClient
from bson.objectid import ObjectId

from db.db import get_db
from db.models import Task
from db import db_qry
from db import alter_data


todo_router = APIRouter()

@todo_router.get('/read-tasks')
def read_tasks(response: Response, db: MongoClient = Depends(get_db)):
    todo_list = db_qry.todos(db)
    response.status_code = status.HTTP_200_OK
    if len(todo_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    return {'todo_list': todo_list}

@todo_router.get('/read-task/{id}')
def read_task_by_id(response: Response, id: str, db: MongoClient = Depends(get_db)):
    res = db_qry.todo(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return res

@todo_router.post('/create-task')
def create_task(response: Response, task: Task, db: MongoClient = Depends(get_db)):
    alter_data.create_task(db, task)
    response.status_code = status.HTTP_201_CREATED
    return True

@todo_router.put('/update-task/{id}')
def update_task(response: Response, id: str, task: Task, db: MongoClient = Depends(get_db)):
    res = alter_data.update_task(db, id, task)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True

@todo_router.put('/update-status/{id}')
def update_status(response: Response, id: str, db: MongoClient = Depends(get_db)):
    res = db_qry.todo(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    alter_data.update_status(db, id, res['is_active'])
    response.status_code = status.HTTP_200_OK
    return True


@todo_router.delete('/delete-task/{id}')
def delete_task(response: Response, id: str, db: MongoClient = Depends(get_db)):
    res = alter_data.delete_task(db, id)
    if not res:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'Error': 'Element with this id does not found'}
    response.status_code = status.HTTP_200_OK
    return True
    

