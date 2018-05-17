from untertaxi_api import password


def test_digested_str():
    s1 = password.digested_str('foo')
    s2 = password.digested_str('foo')
    s3 = password.digested_str('foO')
    assert s1 == s2
    assert s2 != s3


def test_eq():
    h = password.digested_str('foo')
    assert password.eq(h, 'foo')
    assert not password.eq(h, 'foO')
    assert not password.eq('foo', 'foo')
