from qlient.core import GraphQLResponse, GraphQLSubscriptionRequest

from qlient.http.models import GraphQLSubscriptionResponse


def test_http_client_query(qlient_http_client):
    response = qlient_http_client.query.getBooks(["title", "author"])
    assert isinstance(response, GraphQLResponse)
    assert isinstance(response.data["getBooks"], list)


def test_http_client_mutation(qlient_http_client):
    response = qlient_http_client.mutation.addBook(
        ["title", "author"], title="1984", author="George Orwell"
    )
    assert isinstance(response, GraphQLResponse)
    assert isinstance(response.data["addBook"], dict)
    assert response.data["addBook"] == {"title": "1984", "author": "George Orwell"}


def test_async_client_subscription(qlient_http_client):
    count = 0
    response = qlient_http_client.subscription.count(
        target=3, _subscription_id="123", _options={"foo": "bar"}
    )
    assert isinstance(response, GraphQLSubscriptionResponse)
    assert isinstance(response.request, GraphQLSubscriptionRequest)
    assert response.request.subscription_id == "123"
    assert response.request.options == {"foo": "bar"}
    for num in response:
        assert count == num.data["count"]
        count += 1

    assert count == 3


def test_async_client_subscription_with_auto_sub_id(qlient_http_client):
    response = qlient_http_client.subscription.count(target=3)
    assert isinstance(response, GraphQLSubscriptionResponse)
    assert isinstance(response.request, GraphQLSubscriptionRequest)
    assert isinstance(response.request.subscription_id, str)
    response.close()

