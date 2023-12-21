from graphene_pydantic import PydanticObjectType
from pydantic import BaseModel

class PlayerModel(BaseModel):
    player_id: str
    name: str
    position: str
    number: int
    current_Team: str
    height: str
    weight: str
    age: int
    college: str

class PlayerGrapheneModel(PydanticObjectType):
    class Meta:
        model = PlayerModel