from fastapi import APIRouter, File, UploadFile
import os
import time
from hashlib import md5
from typing import List


uploads_router = APIRouter()


@uploads_router.post('/binary-file')
def binary_file(file: bytes = File()):
    return {'file-size': len(file)}

@uploads_router.post('/original-file')
def original_file(file_list: List[UploadFile] = File()):
    folder_path = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(folder_path, exist_ok=True)
    filename_list = []
    for file in file_list:
        uid = md5(str(int(time.time())).encode()).hexdigest()
        file_location = os.path.join(folder_path, f'{uid}_{file.filename}')
        with open(file_location, 'wb') as f:
            f.write(file.file.read())
        filename_list.append(f'{uid}_{file.filename}')
    return {'filename_list': filename_list}