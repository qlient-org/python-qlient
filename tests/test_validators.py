def test_is_local_path():
    from qlient.validators import is_local_path
    assert is_local_path(".")

    assert not is_local_path("http://test.test/graphql")
    assert not is_local_path("https://test.test/graphql")
    assert not is_local_path("file://test/test.json")
