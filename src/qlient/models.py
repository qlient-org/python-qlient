from qlient.types import (
    GraphQLVariables,
    GraphQLQuery,
    GraphQLOperation,
    GraphQLErrors,
    GraphQLExtensions,
    GraphQLData,
    GraphQLReturnType
)


class GraphQLResponse:

    def __init__(
            self,
            response: GraphQLReturnType,
            query: GraphQLQuery,
            variables: GraphQLVariables = None,
            operation_name: GraphQLOperation = None,
    ):
        self.raw: GraphQLReturnType = response

        # request information
        self.query: GraphQLQuery = query
        self.variables: GraphQLVariables = variables
        self.operation_name: GraphQLOperation = operation_name

        # response parsing
        self.data: GraphQLData = self.raw.get("data")
        self.errors: GraphQLErrors = self.raw.get("errors")
        self.extensions: GraphQLExtensions = self.raw.get("extensions")
