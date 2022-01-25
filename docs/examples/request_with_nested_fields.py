from qlient import Client, Fields

client: Client = Client("https://swapi-graphql.netlify.app/.netlify/functions/index")

nested_fields = Fields(
    people=Fields(
        "id",
        "name",
        homeworld="name"
    )
)

response = client.query.allPeople(first=3, _fields=nested_fields)

print(response.query)
# query allPeople($first: Int) { allPeople(first: $first) { people { id name homeworld { name } } } }
