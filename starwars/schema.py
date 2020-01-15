import graphene

from data import setup, get_character, get_droid, get_hero, get_human


class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


class Character(graphene.Interface):
    id = graphene.ID()
    name = graphene.String()
    friends_id = graphene.List(graphene.ID)
    appears_in = graphene.List(Episode)

    friends = graphene.List(lambda: Character)

    def resolve_friends(self, info):
        # The character friends is a list of strings
        return [get_character(f) for f in self.friends_id]


class Human(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    home_planet = graphene.String()


class Droid(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    primary_function = graphene.String()


class Query(graphene.ObjectType):
    hero = graphene.Field(Character, episode=Episode())
    human = graphene.Field(Human, id=graphene.String())
    droid = graphene.Field(Droid, id=graphene.String())
    character = graphene.Field(Character, id=graphene.String())

    def resolve_hero(self, info, episode=None):
        return get_hero(episode)

    def resolve_human(self, info, id):
        return get_human(id)

    def resolve_droid(self, info, id):
        return get_droid(id)
    
    def resolve_character(self, info, id):
        return get_character(id)


schema = graphene.Schema(query=Query,types=[Human, Droid])

if __name__ == "__main__":
    setup()

    query = """
        query HeroNameQuery {
          character(id:"2001"){
              name
              friendsId
          }
        }
    """
    result = schema.execute(query)
    print(result.errors)
    print(result.data)