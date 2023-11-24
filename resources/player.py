from pydantic import BaseModel
import sqlalchemy as db_al
import os
import requests
from dotenv import load_dotenv


# https://pypi.org/project/python-dotenv/
load_dotenv()


# define a Pydantic data model for a player
class PlayerModel(BaseModel):
    player_id: str
    name: str
    position: str = None
    number: int = None
    current_Team: str = None
    height: str = None
    weight: int = None
    age: int = None
    college: str = None

# class to interact with the database for player-related operations
class PlayerResource:
    # constructor
    def __init__(self):
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = str(os.getenv("DB_PORT"))
        db_name = os.getenv("DB_NAME")

        # following based on https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples

        # create a SQLAlchemy engine https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
        db_url = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        # print(db_url) # debugging purpose
        self.engine = db_al.create_engine(db_url)

        self.conn = self.engine.connect()

        self.metadata = db_al.MetaData()  # meta data instance for extracting the metadata: structures, table infos etc

        # table object for player_basic
        self.player_basic = db_al.Table('player_basic', self.metadata, autoload_with=self.engine)

    """
    function to retrieve player information by player ID from the database
    @param player_id: the player id
    @return result: a list of tuple(s)
    """
    def get_player_by_id(self, player_id):
        query = self.player_basic.select().where(self.player_basic.columns.player_id == player_id)
        exe = self.conn.execute(query)  # executing the query
        result = exe.fetchall()
        return result


    

