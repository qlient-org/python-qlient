from qlient import Client

my_client = Client("https://...")

my_query = """
query {
    user1: user(id: "1234") {
        ...userInformation
    }
    user2: user(id: "5678") {
        ...userInformation
    }
}

fragment userInformation on user {
    username
    firstname
    lastname
}
"""

response = my_client.query(query=my_query)
