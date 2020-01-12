from graphene import ObjectType, String, Field, Schema, Dynamic

class Person(ObjectType):
    first_name = String(default_value="Leia")
    last_name = String(default_value="Skywalker")
    full_name = String()
    #See the following issue for the fix below https://github.com/graphql-python/graphene/issues/110, answer by sanfilippopablo
    sibling = Field(lambda: Person)

    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"
    
    def resolve_sibling(parent,info):
        if parent.first_name == "Luke":
            return Person(first_name = "Leia", last_name=parent.last_name)
        else:
            return Person(first_name = "Luke", last_name=parent.last_name)


class Query(ObjectType):
    me = Field(Person)

    def resolve_me(parent, info):
        # returns an object that represents a Person
        return Person(first_name="Leia",last_name="Skywalker")

schema = Schema(query=Query)

query_string = "{ me{fullName sibling {fullName sibling {fullName}}} }"
result = schema.execute(query_string)

#Test that my siblings sibling is me.
assert result.data["me"]["fullName"] == result.data["me"]["sibling"]["sibling"]["fullName"]