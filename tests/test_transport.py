def test_default_transport():
    from qlient.transport import Transport
    from requests.sessions import Session

    transport = Transport()
    assert isinstance(transport.session, Session)
    assert transport.session is not Session()
