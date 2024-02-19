from fastapi import Header, status, HTTPException


secret_token = 'TOKEN'

def validate_token(token: str = Header()):
    if token != secret_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)