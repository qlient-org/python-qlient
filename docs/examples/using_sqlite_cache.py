from qlient import Client, Settings
from qlient.cache import SqliteCache

client = Client("https://...", cache=SqliteCache())

# or with custom settings

settings = Settings(
    json_loads=...,  # uses json.loads by default, can be overwritten to ujson.loads
    json_dumps=...,  # and ujson.dumps
)

client = Client(
    "https://...",
    cache=SqliteCache(
        path="/path/to/my/schema_cache.sqlite",
        expires_in=86400,  # seconds
        settings=settings,
    )
)
