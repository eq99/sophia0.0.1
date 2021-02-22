import json


def test_home(app):
    client = app.test_client()
    res = client.get('/')
    data = res.data.decode()
    assert res.status_code == 200
    assert 'Book list' in data
