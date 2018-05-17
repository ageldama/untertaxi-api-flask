
def test_hello(flask_client):
    "Test `GET /hello/` endpoint"
    assert flask_client is not None
    resp = flask_client.get('/hello/')
    assert resp.status_code == 200
