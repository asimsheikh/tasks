import pytest 

from app import app as flask_app

@pytest.fixture()
def app():
    app = flask_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_posting_form_data(client):
    response = client.post('/testing', data=dict(fname='Asim', lname='Sheikh'))
    assert b'<h1>Asim Sheikh</h1>' in response.data
    


