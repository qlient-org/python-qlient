from qlient import Client, GraphQLResponse

client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

res: GraphQLResponse = client.query.film(
    # swapi graphql input fields
    id="ZmlsbXM6MQ==",

    # qlient specific
    _fields=["id", "title", "episodeID"]
)

print(res.query)  # query film($id: ID) { film(id: $id) { id title episodeID } }
print(res.variables)  # {'id': 'ZmlsbXM6MQ=='}
print(res.data)  # {'film': {'id': 'ZmlsbXM6MQ==', 'title': 'A New Hope', 'episodeID': 4}}
