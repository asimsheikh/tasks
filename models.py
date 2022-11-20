from pydantic import BaseModel, Field

from uuid import uuid4

class Task(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str 
    completed: bool = False
    pomodoros: int = 0