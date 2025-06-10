from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola mundo!'}


def test_read_root_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<h1>Ola mundo!</h1>' in response.text
    assert '<title>Exemplo de HTML Response</title>' in response.text


def test_create_user(client):
    user_data = {
        'username': 'testuser',
        'email': 'test@mail.com',
        'password': 'testpassword',
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert response.json()['id'] == 1


def test_read_users_empty(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_one_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


""" TODO: fixit!!!
def test_read_user_sucess(client):
    test_id = 1
    response = client.get(f'/users/{test_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == test_id
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == 'test@mail.com'
"""


""" TODO: fixit!!!
def test_read_user_failure_id(client):
    test_id = 0
    response = client.get(f'/users/{test_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
"""


def test_update_user_sucess(client, user):
    update_data = {
        'username': 'updateduser',
        'email': 'updated@mail.com',
        'password': 'updatedpwd',
    }
    response = client.put('/users/1', json=update_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'updateduser',
        'email': 'updated@mail.com',
        'id': 1,
    }


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    fausto_data = {
        'username': 'fausto',
        'email': 'fausto@mail.com',
        'password': 'faustopwd',
    }
    client.post('/users/', json=fausto_data)

    # Alterando o user.username das fixture para "fausto"
    response_update = client.put(
        '/users/1',
        json={
            'username': 'fausto',
            'email': 'test@mail.com',
            'password': 'testpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert (
        response_update.json()['detail'] == 'Username or email already exists'
    )


""" TODO: fixit!!!
def test_update_user_failure_id(client):
    user_data_update = {
        'username': 'updateduser',
        'email': 'updated@mail.com',
        'password': 'updatedpassword',
    }
    test_id = 0
    response = client.put(f'/users/{test_id}', json=user_data_update)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
 """


def test_delete_user_sucess(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}
    response_db = client.get('/users/')
    assert response_db.status_code == HTTPStatus.OK
    assert response_db.json() == {'users': []}


""" TODO: fixit!!!
def test_delete_user_failure_id(client):
    test_id = 0
    response = client.delete(f'/users/{test_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
"""
