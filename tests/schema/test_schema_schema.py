from qlient.schema.types import Type


def test_schema():
    from qlient.schema.schema import Schema
    from __base__ import make_test_schema

    schema = make_test_schema()
    assert isinstance(schema, Schema)
    assert schema.schema_provider.cache_key == "Test"

    assert isinstance(schema.query_type, Type)
    assert schema.query_type.name == "Root"

    assert schema.mutation_type is None

    assert schema.subscription_type is None

    assert schema.cache is None

    assert str(schema) == "<Schema(query_type=<Type(name=`Root`)>, mutation_type=None, subscription_type=None)>"
