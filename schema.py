import graphene

# import from serializers
from serializer import PlayerGrapheneModel

# import from models
from model.model_player import Player

class Query(graphene.ObjectType):
    say_hello = graphene.String(name=graphene.String(default_value="hello"))
    list_all_players = graphene.List(PlayerGrapheneModel)
    get_player_by_id = graphene.Field(PlayerGrapheneModel, player_id=graphene.NonNull(graphene.String))

    @staticmethod
    def resolve_say_hello(parent, info, name):
        return f"hello {name}!"

    @staticmethod
    def resolve_list_all_players(parent, info):
        return Player.all()

    @staticmethod
    def resolve_get_player_by_id(parent, info, player_id):
        return Player.find_or_fail(player_id)