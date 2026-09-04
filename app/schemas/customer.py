from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class CustomerUpdate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class CustomerResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: EmailStr
    phone: str
    address: str

    model_config = ConfigDict(from_attributes=True)