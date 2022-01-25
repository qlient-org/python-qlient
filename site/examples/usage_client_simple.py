from qlient import Client

client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

result = client.query.launchesPast(
    limit=3,
    _fields=["mission_id", "mission_name"]
)