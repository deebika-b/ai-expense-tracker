from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    amount: float
    category: str
    description: str | None = None