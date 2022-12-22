from pydantic import BaseModel, Field, validator

from uuid import uuid4

class Task(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    name: str 
    
    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v
class Pebble(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    pebble_id: int 
    checked: bool = False
    
    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v