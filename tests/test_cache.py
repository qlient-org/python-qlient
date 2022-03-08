# skipcq: PY-D0003
def test_in_memory_cache():
    from qlient.cache import InMemoryCache

    my_cache = InMemoryCache()

    my_cache["test"] = {"foo": "bar"}
    assert "test" in my_cache


# skipcq: PY-D0003
def test_sqlite_cache():
    from qlient.cache import SqliteCache
    my_cache = SqliteCache()
    my_cache["test"] = {"foo": "bar"}
    assert "test" in my_cache


# skipcq: PY-D0003
def test_custom_sqlite_cache():
    import datetime
    from qlient.cache import SqliteCache
    my_cache = SqliteCache(path="/tmp/test_cache.sqlite", expires_in=60 * 60 * 24)
    assert my_cache.path == "/tmp/test_cache.sqlite"
    assert isinstance(my_cache.expires_in, datetime.timedelta)
    assert my_cache.expires_in == datetime.timedelta(days=1)
