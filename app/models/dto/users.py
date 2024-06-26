from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    name: str
    age: int
    passport: str
