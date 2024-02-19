from fastapi import FastAPI, APIRouter, Query, Request
import time
from fastapi.middleware.cors import CORSMiddleware

from todo import todo_router
from user import user_router
from category import category_router
from upload_router import uploads_router


app = FastAPI()
router = APIRouter()

@app.middleware('http')
async def add_processing_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers['Processing-Time'] = str(time.time() - start_time)
    return response

origins = [
    "http://site.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(todo_router, prefix='/todos')
app.include_router(uploads_router, prefix='/uploads')
app.include_router(user_router, prefix='/users')
app.include_router(category_router, prefix='/categories')



