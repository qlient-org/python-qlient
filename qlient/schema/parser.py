""" 

:author: Daniel Seifert
:created: 10.09.2021
:copyright: Swisscom
"""
from typing import Dict, Optional

from qlient.schema.models import Type, Directive


class ParseResult:
    """ Represents a parsed graphql schema """

    def __init__(
            self,
            query_type: Optional[Type] = None,
            mutation_type: Optional[Type] = None,
            subscription_type: Optional[Type] = None,
            types: Optional[Dict[str, Type]] = None,
            directives: Optional[Dict[str, Directive]] = None
    ):
        self.query_type: Optional[Type] = query_type
        self.mutation_type: Optional[Type] = mutation_type
        self.subscription_type: Optional[Type] = subscription_type
        self.types: Optional[Dict[str, Type]] = types
        self.directives: Optional[Dict[str, Directive]] = directives


def extract_type(type_name: str, types: Optional[Dict[str, Type]]) -> Optional[Type]:
    """ Extract a type from all types """
    if types is None:
        return None
    return types.get(type_name)


def extract_query_type(schema: Dict, types: Optional[Dict[str, Type]]) -> Optional[Type]:
    """ Extract the name of the query type from the schema """
    query_type = schema.get("queryType", {}).get("name")
    return extract_type(query_type, types)


def extract_mutation_type(schema: Dict, types: Optional[Dict[str, Type]]) -> Optional[Type]:
    """ Extract the name of the mutation type from the schema """
    mutation_type = schema.get("mutationType", {}).get("name")
    return extract_type(mutation_type, types)


def extract_subscription_type(schema: Dict, types: Optional[Dict[str, Type]]) -> Optional[Type]:
    """ Extract the name of the subscription type from the schema """
    subscription_type = schema.get("subscriptionType", {}).get("name")
    return extract_type(subscription_type, types)


def parse_types(schema: Dict) -> Optional[Dict[str, Type]]:
    return None


def parse_directives(schema: Dict) -> Optional[Dict[str, Directive]]:
    return None


def parse_schema(schema: Dict) -> ParseResult:
    """ Parse the given graphql schema and return the parsed result

    :param schema: holds the raw schema as a dictionary
    :return: parse result with all types, directives and stuff
    """
    types = parse_types(schema)
    return ParseResult(
        query_type=extract_query_type(schema, types),
        mutation_type=extract_mutation_type(schema, types),
        subscription_type=extract_subscription_type(schema, types),
        types=types,
        directives=parse_directives(schema)
    )
