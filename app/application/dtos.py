from pydantic import BaseModel, EmailStr, Field
import uuid
from typing import Optional
from datetime import datetime


class UserSellerCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    cpf: str

    class Config:
        orm_mode = True


class UserSellerResponseDTO(BaseModel):
    id: str
    name: str
    email: EmailStr
    cpf: str

    class Config:
        orm_mode = True


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class OrderCreateDTO(BaseModel):
    cod: str
    status: str = Field(default="Em validação")
    amount: float
    user_id: Optional[str] = None
    seller_cpf: str


class OrderResponseDTO(BaseModel):
    id: str
    cod: str
    status: str
    user_id: str
    created_at: datetime
    amount: float
    seller_cpf: str
    cashback_percentage: float = 0.10
    cashback_amount: float = 0.0

    def calculate_cashback(self):
        self.cashback_amount = round(self.amount * self.cashback_percentage, 2)

    class Config:
        orm_mode = True
