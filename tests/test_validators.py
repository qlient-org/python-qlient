def test_is_local_path():
    from qlient.validators import is_local_path
    assert is_local_path(".")
    assert is_local_path("/")
    assert is_local_path("/tmp")


def test_is_not_local_path():
    from qlient.validators import is_local_path

    assert not is_local_path("http://test.test/graphql")
    assert not is_local_path("https://test.test/graphql")
    assert not is_local_path("file://test/test.json")


def test_is_url():
    from qlient.validators import is_url
    assert is_url("http://test.test/graphql")
    assert is_url("https://google.com")
    assert is_url("https://api.spacex.land/graphql/")


def test_is_not_url():
    from qlient.validators import is_url
    assert not is_url(".")
    assert not is_url("./schema.json")
    assert not is_url("/")
    assert not is_url("/tmp/schema.json")
