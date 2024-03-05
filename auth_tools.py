from fastapi import Header, status, HTTPException
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer

from db import db_qry


pwd_context = CryptContext(schemes=['bcrypt'])
secret_key = 'secret_key'
algorythm = 'HS256'
auth_schema = OAuth2PasswordBearer(tokenUrl='/users/token')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(pasword: str, hashed_password: str):
    return pwd_context.verify(pasword, hashed_password)

def cerate_access_token(login_data):
    return jwt.encode(login_data, key=secret_key, algorithm=algorythm)

def verify_token(db, token):
    user_data = jwt.decode(token, key=secret_key, algorithms=algorythm)
    if user_data.get('email') is not None:
        user = db_qry.user(db, email=user_data['email'])
        return user
    return None

def authenticate_user(db, email, password):
    user = db_qry.user(db, email=email)
    if user is None:
        return False
    if not verify_password(password, user['password']):
        return False
    return user
