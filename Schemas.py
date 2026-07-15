from pydantic import BaseModel
from typing import Literal

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: Literal["user", "employee"]


class UserLogin(BaseModel):
    email: str
    password: str


class ProductCreate(BaseModel):
    name: str
    price: int


class CartCreate(BaseModel):
    product_id: int
    quantity: int


class CartUpdate(BaseModel):
    quantity: int


class DeleteCart(BaseModel):
    quantity: int

class Checkout(BaseModel):
    user_id: int