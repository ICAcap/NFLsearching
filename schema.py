import graphene
from graphene import ObjectType, ID, String, List
from serializer import PlayerGrapheneModel
from model.model_player import Player

# import from serializers
from serializer import PlayerGrapheneModel

# import from models
from model.model_player import Player

class PlayerQuery(graphene.ObjectType):
    say_hello = graphene.String(name=graphene.String(default_value="hello"))
    list_all_players = graphene.List(PlayerGrapheneModel)
    get_player_basic_info = List(PlayerGrapheneModel,
                                 player_id=ID(),
                                 name=String(),
                                 position=String(),
                                 number=String(),
                                 current_team=String(),
                                 height=String(),
                                 weight=String(),
                                 age=String(),
                                 college=String())

    @staticmethod
    def resolve_say_hello(parent, info, name):
        return f"hello {name}!"

    @staticmethod
    def resolve_list_all_players(parent, info):
        return Player.all()

    @staticmethod
    def resolve_get_player_basic_info(parent, info, **kwargs):
        # Filter players based on the provided parameters
        query = Player.query()
        for field, value in kwargs.items():
            if value:
                query = query.where(field, value)
        return query.get()
