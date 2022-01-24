from qlient import Client

client = Client("https://...")

res = client.query.myQuery("foo")

type(res)  # <class 'qlient.response.QlientResponse'>
type(res.response)  # <class 'requests.models.Response'>

# What follows next are GraphQL specific response attributes
# Checkout https://spec.graphql.org/June2018/#sec-Response for more information.
#
# Let's say the server returns the following:
# {
#   "data": {
#     "myQuery": {
#       "foo": "bar"
#     }
#   },
#   "errors": [],
#   "extensions": []
# }
# This would be mapped like so:

print(res.data)  # {"myQuery": {"foo": "bar"}}
print(res.errors)  # []
print(res.extensions)  # []
