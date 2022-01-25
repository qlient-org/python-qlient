from qlient import Client
from qlient.cache import InMemoryCache

client = Client("https://...", cache=InMemoryCache())
