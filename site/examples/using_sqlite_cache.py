from qlient import Client
from qlient.cache import SqliteCache

client = Client("https://...", cache=SqliteCache())

# or with custom settings

client = Client(
    "https://...",
    cache=SqliteCache(
        path="/path/to/my/schema_cache.sqlite",
        expires_in=86400  # seconds
    )
)
