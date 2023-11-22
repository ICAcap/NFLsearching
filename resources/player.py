from typing import List

# class definition
class Player:
    # players don't get to pick their id, it will be assigned by the db
    def __int__(self, name: str, position: str=None, number: int=None, current_Team: str=None, height: str=None
                , weight: int=None, age: int=None, college: str=None):
        self.name = name
        self.number = number
        self.current_Team = current_Team
        self.height = height
        self.weight = weight
        self.age = age
        self.college = college
