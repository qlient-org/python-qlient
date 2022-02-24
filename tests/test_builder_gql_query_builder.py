def test_query_builder():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder()
    expected = "{ }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_operation_query():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().operation("query")
    expected = "query { }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_operation_query_name():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().operation("query", name="MyQuery")
    expected = "query MyQuery { }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_operation_query_name_variables():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().operation("query", name="MyQueryVar", variables={"$foo": "String!"})
    expected = "query MyQueryVar($foo: String!) { }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_operation_mutation():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().operation("mutation")
    expected = "mutation { }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_operation_mutation_name():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().operation("mutation", name="MyMutation")
    expected = "mutation MyMutation { }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_operation_mutation_name_variables():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().operation("mutation", name="MyMutationVar", variables={"$foo": "String!"})
    expected = "mutation MyMutationVar($foo: String!) { }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_action():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().action("foo")
    expected = "{ foo }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_action_variables():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder().action("foo", variables={"bar": 1})
    expected = "{ foo(bar: 1) }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_fields_simple():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder()
    builder = builder.action("get_person")
    builder = builder.fields("first_name last_name")
    expected = "{ get_person { first_name last_name } }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_full_query():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder()
    builder = builder.operation("query", name="PersonQuery", variables={"$search": "String"})
    builder = builder.action("get_person", variables={"search": "$search"})
    builder = builder.fields("first_name last_name hobby { title description }")
    expected = "query PersonQuery($search: String) { get_person(search: $search) { first_name last_name hobby { title description } } }"
    actual = builder.build()
    assert expected == actual


def test_query_builder_full_mutation():
    from qlient.builder import GQLQueryBuilder
    builder = GQLQueryBuilder()
    builder = builder.operation("mutation", name="UpdatePerson", variables={"$id": "ID!"})
    builder = builder.action("update_person", variables={"id": "$id"})
    builder = builder.fields("first_name last_name")
    expected = "mutation UpdatePerson($id: ID!) { update_person(id: $id) { first_name last_name } }"
    actual = builder.build()
    assert expected == actual
