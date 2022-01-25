from qlient import Client

client = Client("https://my-graphql-api.com/")

# query is a QueryService object (Inherits from OperationProxy). It will check if there
# is an operation with the name `X` defined in the binding
# and if that is the case it will return a callable Operation object
client.query.X()

# The operation can also be called via an __getitem__ call.
# This is useful if the operation name is not a valid
# python attribute name.
client.query["X-Y-Z"]()

# in GraphQL, you can do more than just query data.
# for example mutations.
client.mutation.changeX()

# Subscriptions are not yet supported.
