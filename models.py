from pydantic import BaseModel, Field, validator

from uuid import uuid4

class Task(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    name: str 
    completed: bool = False
    pomodoros: int = 0
    
    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v


class Notes(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    date: str
    text: str
    task_id: str 

class Contact(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    first_name: str
    last_name: str
    email: str 

    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v