from qlient import Client

client = Client("https://api.spacex.land/graphql/")

res = client.query.launchesPast(
    # spacex graphql input fields
    find={"mission_name": "Starlink"},
    limit=5,
    sort="mission_name",

    # qlient specific
    _fields=["mission_name", "launch_success", "launch_year"]
)
