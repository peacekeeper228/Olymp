from pydantic import BaseModel
from typing import Optional

class Group(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

class Participant(BaseModel):
    id: Optional[int] = None
    name: str
    wish: Optional[str] = None
    def __eq__(self, other):
        if self.id==other.id:
            return True
        else:
            return False

class ParticipantsInGroups(BaseModel):
    GroupID: Optional[int] = None
    ParticipantID: Optional[int] = None

class Recipients(BaseModel):
    Person: Optional[Participant] = None
    Recipient: Optional[Participant] = None

