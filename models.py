from datetime import datetime
from pydantic import BaseModel, Field

from uuid import uuid4

class Task(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str 
    completed: bool = False
    pomodoros: int = 0


class Notes(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    date: datetime = Field(default_factory=datetime.now)
    text: str
    task_id: str 