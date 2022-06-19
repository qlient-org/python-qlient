"""This module contains utility functions that are used across the package."""


def convert_to_websocket_url(url: str) -> str:
    """Function to convert a http url to a websocket url by replacing the protocol.

    Args:
        url: holds the url to convert

    Returns:
        the converted url

    Examples:
        Usage with https
        >>> convert_to_websocket_url("https://qlient.com")  #  wss://qlient.com

        Usage with http
        >>> convert_to_websocket_url("http://qlient.com")  # ws://qlient.com
    """
    if url.startswith("https://"):
        return url.replace("https://", "wss://")
    if url.startswith("http://"):
        return url.replace("http://", "ws://")
    raise ValueError(
        f"URL '{url}' does neither start with 'https://' nor with 'http://'."
    )
