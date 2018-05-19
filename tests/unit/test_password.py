from untertaxi_api import password


def test_hash_password():
    secret = 'SECRET'
    s1 = password.hash_password('foo', secret)
    s2 = password.hash_password('foo', secret)
    s3 = password.hash_password('foO', secret)
    assert s1 == s2
    assert s2 != s3

