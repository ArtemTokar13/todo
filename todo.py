from fastapi import APIRouter, Body
from models import Task


todo_router = APIRouter()
todo_list = []


@todo_router.get('/read-tasks')
def read_tasks():
    return {'todo_list': todo_list}

@todo_router.post('/create-task')
def create_task(task: Task):
    todo_list.append(task)
    return {'todo_list': todo_list}

@todo_router.put('/update-task/{id}/{task}')
def update_task(id: int, task: str):
    todo_list[id] = task
    return {'todo_list': todo_list}

@todo_router.delete('/delete-task/{id}')
def delete_task(id: int):
    del todo_list[id]
    return {'todo_list': todo_list}