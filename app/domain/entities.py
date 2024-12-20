from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSeller(BaseModel):
    id: str
    email: EmailStr
    password: str
    cpf: str
    name: str
