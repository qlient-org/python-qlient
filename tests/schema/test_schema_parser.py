def test_parse_schema_types():
    from qlient.schema.parser import parse_types
    from __base__ import raw_schema
    schema = raw_schema["data"]["__schema"]
    types = parse_types(schema)
    assert isinstance(types, dict)


def test_query_type_extraction():
    from qlient.schema.parser import parse_types, extract_query_type
    from qlient.schema.types import Type
    from __base__ import raw_schema
    schema = raw_schema["data"]["__schema"]
    types = parse_types(schema)
    query_type = extract_query_type(schema, types)
    assert isinstance(query_type, Type)


def test_mutation_type_extraction():
    from qlient.schema.parser import parse_types, extract_mutation_type
    from __base__ import raw_schema
    schema = raw_schema["data"]["__schema"]
    types = parse_types(schema)
    mutation_type = extract_mutation_type(schema, types)
    assert mutation_type is None


def test_subscription_type_extraction():
    from qlient.schema.parser import parse_types, extract_subscription_type
    from __base__ import raw_schema
    schema = raw_schema["data"]["__schema"]
    types = parse_types(schema)
    subscription_type = extract_subscription_type(schema, types)
    assert subscription_type is None


def test_parse_schema_directives():
    from qlient.schema.parser import parse_directives
    from __base__ import raw_schema
    schema = raw_schema["data"]["__schema"]
    directives = parse_directives(schema)
    assert isinstance(directives, dict)


def test_empty_parse_result():
    from qlient.schema.parser import ParseResult
    empty_result = ParseResult()
    assert empty_result.query_type is None
    assert empty_result.mutation_type is None
    assert empty_result.subscription_type is None
    assert empty_result.types is None
    assert empty_result.directives is None


def test_filled_parse_result():
    from qlient.schema.parser import ParseResult
    from qlient.schema.types import Type
    empty_result = ParseResult(
        query_type=Type(name="Query"),
        mutation_type=Type(name="Mutation"),
        subscription_type=Type(name="Subscription"),
        types={},
        directives={}
    )
    assert empty_result.query_type.name == "Query"
    assert empty_result.mutation_type.name == "Mutation"
    assert empty_result.subscription_type.name == "Subscription"
    assert empty_result.types == {}
    assert empty_result.directives == {}


def test_parse_schema():
    from qlient.schema.parser import parse_schema, ParseResult
    from __base__ import raw_schema
    schema = raw_schema["data"]["__schema"]
    parse_result: ParseResult = parse_schema(schema)
    assert isinstance(parse_result, ParseResult)
    assert parse_result.query_type is not None
    assert parse_result.mutation_type is None
    assert parse_result.subscription_type is None
