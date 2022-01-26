from qlient.schema.types import RawSchema


def test_schema_loader():
    from qlient.schema.providers import StaticSchemaProvider
    from qlient.schema.loader import load_schema

    schema = load_schema(StaticSchemaProvider({"foo": "bar"}, "foo"), cache=None)
    assert schema == {"foo": "bar"}


def test_schema_loader_cached():
    from qlient.schema.providers import StaticSchemaProvider
    from qlient.cache import InMemoryCache
    from qlient.schema.loader import load_schema

    class MyProvider(StaticSchemaProvider):
        def __init__(self):
            super(MyProvider, self).__init__({"foo": "bar"}, "foo")
            self.load_schema_called = 0

        def load_schema(self) -> RawSchema:
            self.load_schema_called += 1
            return super().load_schema()

    cache = InMemoryCache()
    provider = MyProvider()

    schema = load_schema(provider, cache)  # should load from provider
    assert schema == {"foo": "bar"}
    assert provider.load_schema_called == 1

    schema = load_schema(provider, cache)  # loads from cache
    assert schema == {"foo": "bar"}
    assert provider.load_schema_called == 1
