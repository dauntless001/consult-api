from fastapi import HTTPException


def get_message(text:str, code:int):
    return HTTPException(
        status_code=code,
        detail = text,
        headers={"WWW-Authenticate":'Bearer'}
)
