def test_graphql_response():
    from qlient.models import GraphQLResponse

    query = "query testOperation { testOperation { foo bar } }"
    variables = {"limit": 1}
    operation_name = "testOperation"
    response_body = {"data": {"testOperation": {"foo": "", "bar": ""}}, "errors": [], "extensions": []}
    qlient_response = GraphQLResponse(response_body, query, variables, operation_name)

    assert qlient_response.variables == variables
    assert qlient_response.raw == response_body

    assert qlient_response.query == query
    assert qlient_response.variables == variables
    assert qlient_response.operation_name == operation_name

    assert qlient_response.data == {"testOperation": {"foo": "", "bar": ""}}
    assert qlient_response.errors == []
    assert qlient_response.extensions == []
