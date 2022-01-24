import io


def test_base_response():
    import requests
    from qlient.response import BaseResponse
    qlient_response = BaseResponse(requests.Response())
    assert isinstance(qlient_response.response, requests.Response)


def test_graphql_response():
    import requests
    request_payload = {
        "query": "query testOperation { testOperation { foo bar } }",
        "variables": {"limit": 1},
        "operationName": "testOperation"
    }
    request = requests.Request("POST", "https://mygraphql.api/", json=request_payload)
    response = requests.Response()
    response.raw = io.BytesIO(b'{"data": {"testOperation": {"foo": "", "bar": ""}}, "errors": [], "extensions": []}')
    response.status_code = 200
    response.request = request.prepare()
    # response faking done

    from qlient.response import GraphQLResponse

    qlient_response = GraphQLResponse(response)

    assert qlient_response.response is response

    assert qlient_response.request_content == request_payload
    assert qlient_response.response_content == {
        "data": {
            "testOperation": {
                "foo": "",
                "bar": ""
            }
        },
        "errors": [],
        "extensions": []
    }

    assert qlient_response.query == request_payload["query"]
    assert qlient_response.variables == request_payload["variables"]
    assert qlient_response.operation_name == request_payload["operationName"]

    assert qlient_response.data == {"testOperation": {"foo": "", "bar": ""}}
    assert qlient_response.errors == []
    assert qlient_response.extensions == []
