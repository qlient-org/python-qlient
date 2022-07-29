from qlient import Fields, Field, Directive

my_home_world_selection = Fields("id", "name", "population")

my_person_selection = Fields(
    "id",  # will be converted to Field("id")
    Field("name"),
    Field("height", _alias="my_height"),
    Field(
        "homeworld",
        _sub_fields=my_home_world_selection,
        _directive=Directive("include", **{"if": True}),
    ),
)

# Every variable name used in a Field or Directive is automatically generated and therefore unique.
# {
#     id
#     name
#     my_height: height
#     homeworld @include(if: $include_123456789_if) {
#         id
#         name
#         population
#     }
# }
