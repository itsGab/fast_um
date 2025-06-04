from http import HTTPStatus


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
    response_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert response_data['username'] == user_data['username']
    assert response_data['email'] == user_data['email']
    assert 'user_id' in response_data
    assert response_data['user_id'] > 0


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    for user in response.json()['users']:
        assert 'user_id' in user
        assert 'username' in user
        assert response.json()['users'][0]['username'] == 'testuser'
        assert 'email' in user
        assert 'password' not in user  # password should not be returned


def test_update_user_sucess(client):
    user_data_update = {
        'username': 'updateduser',
        'email': 'updated@mail.com',
        'password': 'updatedpassword',
    }
    test_id = 1
    response = client.put(f'/users/{test_id}', json=user_data_update)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user_data_update['username']
    assert response.json()['email'] == user_data_update['email']


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


# TODO: Implementar testes para update e delete
def test_delete_user_sucess(client):
    test_id = 1
    response = client.delete(f'/users/{test_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}

    # Verifica se o usuário foi realmente removido
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    for user in response.json()['users']:
        assert user['user_id'] != test_id


def test_delete_user_failure_id(client):
    test_id = 0
    response = client.delete(f'/users/{test_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# TODO: delete after fixing database
def test_get_fake_database(client):
    response = client.get('/database/')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    for user in response.json():
        assert 'user_id' in user
        assert 'username' in user
        assert 'email' in user
        assert 'password' in user
