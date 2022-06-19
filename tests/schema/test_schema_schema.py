from qlient.schema.types import Type


# skipcq: PY-D0003
def test_schema(swapi_schema):
    from qlient.schema.schema import Schema

    assert isinstance(swapi_schema, Schema)
    assert swapi_schema.schema_provider.cache_key == "Test"

    assert isinstance(swapi_schema.query_type, Type)
    assert swapi_schema.query_type.name == "Root"

    assert swapi_schema.mutation_type is None

    assert swapi_schema.subscription_type is None

    assert swapi_schema.cache is None

    assert str(swapi_schema) == "<Schema(query_type=<Type(name=`Root`)>, mutation_type=None, subscription_type=None)>"
