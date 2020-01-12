from graphene import ObjectType, String, Schema, Int
from graphene import List as graphene_list

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = Int(number_one=Int(default_value=0),number_two=Int(default_value=0))
    goodbye = graphene_list(Int)

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, number_one,number_two):
        return number_one+number_two

    def resolve_goodbye(root, info):
        return [1,2,3,4]

schema = Schema(query=Query)

# we can query for our field (with the default argument)
query_string = '{ hello}'
result = schema.execute(query_string)
print(str(result.data['hello']))
# "Hello stranger"

# or passing the argument in the query
query_with_argument = '{ hello(numberOne: 5,numberTwo:2) }'
result = schema.execute(query_with_argument)
print(str(result.data['hello']))
# "Hello GraphQL!"

query_with_argument = '{ hello, goodbye }'
result = schema.execute(query_with_argument)
print(str(result.data['hello']))