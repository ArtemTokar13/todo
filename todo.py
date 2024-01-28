from fastapi import APIRouter, Response, status
from models import Task


todo_router = APIRouter()
todo_list = []


@todo_router.get('/read-tasks')
def read_tasks(response: Response):
    response.status_code = status.HTTP_200_OK
    if len(todo_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {'todo_list': todo_list}

@todo_router.post('/create-task')
def create_task(response: Response, task: Task):
    for todo in todo_list:
        if todo.id == task.id:
            response.status_code = status.HTTP_409_CONFLICT
            return False
    todo_list.append(task)
    response.status_code = status.HTTP_201_CREATED
    return {'todo_list': todo_list}

@todo_router.put('/update-task/{id}')
def update_task(response: Response, id: int, task: Task):
    for i in range(len(todo_list)):
        if todo_list[i].id == id:
            todo_list[i] = task
            response.status_code = status.HTTP_200_OK
            return {'todo_list': todo_list}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'Error': 'Element with this id does not found'}

@todo_router.delete('/delete-task/{id}')
def delete_task(response: Response, id: int):
    for i in range(len(todo_list)):
        if todo_list[i].id == id:
            del todo_list[i]
            response.status_code = status.HTTP_200_OK
            return {'todo_list': todo_list}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'Error': 'Element with this id does not found'}

