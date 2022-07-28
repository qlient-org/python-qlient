from qlient import Field, Directive

my_field = Field(
    # Mandatory, the name of the field
    "repository",
    # Schema Field specific inputs
    # say we want the last 5 repositories where the name matches abc
    last=5,
    name="*abc*",
    # Qlient Field specific arguments start with a `_`
    # These arguments are Optional and can be left empty
    # Optional, the alias of the field
    _alias="my_repo",
    # Optional, a field directive
    _directive=Directive("include", **{"if": True}),
)

# This results in a field like so:

# {
#   my_repo: repository(last: $repository_1234_last name: $repository_1234_name) @include(if: $include_5678_if)
# }
