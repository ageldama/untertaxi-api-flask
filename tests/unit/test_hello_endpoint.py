
def test_hello(flask_client):
    "Test `GET /hello/` endpoint"
    assert flask_client is not None
    resp = flask_client.get('/hello/')
    assert resp.status_code == 200


from werkzeug.datastructures import Headers
import base64

def add_http_authz_header_base64(headers: 'Headers',
                                 username: str, password: str):
    headers.add('Authorization',
                'Basic ' + base64.b64encode(
                    bytes(username + ":" + password, 'ascii')).decode('ascii'))
    return headers
    
    
def test_restricted(flask_client):
    "Test `GET /hello/restricted` endpoint"
    assert flask_client is not None
    # access denied
    resp = flask_client.get('/hello/restricted')
    assert resp.status_code == 401
    # login ok
    username = 'foo'
    password = 'bar'
    resp = flask_client.get('/hello/restricted',
                            headers=add_http_authz_header_base64(
                                Headers(), username, password))
    assert resp.status_code == 200

# EOF.
