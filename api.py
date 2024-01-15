from fastapi import FastAPI, APIRouter, Query
from todo import todo_router


app = FastAPI()
router = APIRouter()


@app.get('/page')
def page(pg: str=Query(regex='^[0-9]*$')):
    return {'pg': pg}


app.include_router(router)
app.include_router(todo_router, prefix='/todos')

