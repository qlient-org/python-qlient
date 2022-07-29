from qlient.http import HTTPClient, Fields

client = HTTPClient("https://swapi-graphql.netlify.app/.netlify/functions/index")

all_films_fields = Fields(
    "totalCount", films=["id", "title", "director", "releaseDate"]
)

response = client.query.allFilms(all_films_fields)
