from pydantic import BaseModel, AnyUrl


class In(BaseModel):
    name: str
    breed: str
    age: int


class Out(In):
    url: AnyUrl
