from uuid import uuid4
from pydantic import BaseModel
from typing import Optional

from persist import Persist

class User(BaseModel):
    id: Optional[str] = uuid4().hex
    first_name: str
    last_name: str

def test_example():
    assert 2 == 2

def test_adding_user():
    asim = User(first_name='Asim', last_name='Sheikh')
    faizan = User(first_name='Faizan', last_name='Sheikh')
    db = Persist()
    db.clear()
    db.add(key='users', data=asim.dict())
    db.add(key='users', data=faizan.dict())

    assert db.get_all() == {'users': [asim.dict(), faizan.dict()]}



