from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola mundo!'}


def test_read_root_html():
    client = TestClient(app)
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert '<h1>Ola mundo!</h1>' in response.text
    assert '<title>Exemplo de HTML Response</title>' in response.text
