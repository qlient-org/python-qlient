from qlient.http import HTTPClient

client = HTTPClient("https://swapi-graphql.netlify.app/.netlify/functions/index")

response = client.query.allFilms(
    ["id", "title", "episodeID", "director", "releaseDate"],
    id="ZmlsbXM6MQ==",
)
