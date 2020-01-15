#Trying to implement the graphs myself..

import graphene

class Human(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    friends_id = graphene.List(graphene.String)
    appears_in = graphene.List(graphene.Int)
    home_planet = graphene.String(default_value=None)
    primary_function = graphene.String(default_value=None)
    friends = graphene.List(lambda: Human)

    def resolve_friends(self, info):
        return [get_character(fid) for fid in self.friends_id]

class Query(graphene.ObjectType):
    me = graphene.Field(Human,id=graphene.ID(default_value="1000"))

    def resolve_me(self, info, id):
        return get_character(id)

def get_character(id):
    return human_data.get(id) or droid_data.get(id)

human_data = {
    "1000" : Human(id="1000",name="Luke Skywalker",friends_id=["1002", "1003", "2000", "2001"],appears_in=[4, 5, 6],home_planet="Tatooine"),
    "1001" : Human(id="1001",name="Darth Vader",friends_id=["1004"],appears_in=[4, 5, 6],home_planet="Tatooine"),
    "1002" : Human(id="1002",name="Han Solo",friends_id=["1000", "1003", "2001"],appears_in=[4, 5, 6],home_planet=None),
    "1003" : Human(id="1003",name="Leia Organa",friends_id=["1000", "1002", "2000", "2001"],appears_in=[4, 5, 6],home_planet="Alderaan"),
    "1004" : Human(id="1004",name="Wilhuff Tarkin",friends_id=["1001"],appears_in=[4],home_planet=None),
}

droid_data = { 
    "2000" : Human(id="2000",name="C-3PO",friends_id=["1000", "1002", "1003", "2001"],appears_in=[4, 5, 6],primary_function="Protocol"),
    "2001" : Human(id="2001",name="R2-D2",friends_id=["1000", "1002", "1003"],appears_in=[4, 5, 6],primary_function="Astromech")
}

schema=graphene.Schema(query=Query)

query = """
    query testQuery {
        me(id:1000){
            id
            name
            friends{
                name
            }
        }
    }
    """

result = schema.execute(query)
print(result.errors)
print(result.data["me"]["friends"])