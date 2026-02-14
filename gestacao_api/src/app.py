import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from src.routers import auth, DailyMessages, users
from src.schemas.message import Message


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(DailyMessages.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
