# this is for the graphql

from db import Model

class Player(Model):
    # define fields corresponding to the "player_basic" sql table
    # https://orator-orm.com/docs/0.9/orm.html
    __fillable__ = ['player_id', 'name', 'position', 'number', 'current_team', 'height', 'weight', 'age', 'college']