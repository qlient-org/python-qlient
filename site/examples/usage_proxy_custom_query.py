from qlient import Client

my_client = Client("https://...")

foo_bar_query = "query { foo bar }"

result = my_client.query(query=foo_bar_query)
