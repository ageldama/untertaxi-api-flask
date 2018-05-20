# -*- coding: utf-8; -*-
import requests
from requests.auth import HTTPBasicAuth
import json
from faker import Faker

BASE_URL = 'http://127.0.0.1:5000'
FAKER = Faker()

# NEW PASSENGER
email = FAKER.email()
password = "foobarzoospam"

put_member_req = {'email':email, 'password':password, 'member_type':'PASSENGER'}
print(put_member_req)
r = requests.put(BASE_URL + '/v1/member', json=put_member_req)
print(r.status_code, r.text)
assert r.status_code == 201

# AUTH
def hash_password(password: str, secret_key: str) -> str:
    import hashlib
    m = hashlib.sha256()
    m.update(secret_key.encode())
    m.update(password.encode())
    return m.hexdigest()

SECRET_KEY = 'default-secret-key'

auth=HTTPBasicAuth(email, hash_password(password, SECRET_KEY))

# NEW ADDRESS
put_address_req = {'address': FAKER.address()}
print(put_address_req)
r = requests.put(BASE_URL + '/v1/address', json=put_address_req, auth=auth)
print(r.status_code, r.text)
address_id = r.json()['id']
print("new address id: ", address_id)

# NEW RIDE-REQUEST
put_ride_request_req = {'address_id': address_id}
print(put_ride_request_req)
r = requests.put(BASE_URL + '/v1/ride_request', json=put_ride_request_req, auth=auth)
print(r.status_code, r.text)

# LIST RIDE-REQUEST
r = requests.get(BASE_URL + '/v1/ride_request', auth=auth)
print(r.text)

