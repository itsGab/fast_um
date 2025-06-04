from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import (
    Message,
    UserDB,
    UserPublic,
    UserPublicList,
    UserSchema,
)

app = FastAPI()

# * Database fake para testes
fake_database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola mundo!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root_html():
    return """
    <html>
        <head>
            <title>Exemplo de HTML Response</title>
        </head>
        <body>
            <h1>Ola mundo!</h1>
        </body>
    </html>
    """


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), user_id=len(fake_database) + 1)
    fake_database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserPublicList)
def read_users():
    return {'users': fake_database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(fake_database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    user_with_id = UserDB(**user.model_dump(), user_id=user_id)
    fake_database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id > len(fake_database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    fake_database.pop(user_id - 1)
    return {'message': 'User deleted successfully'}


# * Returns fake database for testing purposes
@app.get('/database/', status_code=HTTPStatus.OK, response_model=list[UserDB])
def get_database():
    return fake_database
