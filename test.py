import fastapi
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from models import Base
from database import Base
import Schemas
from employee import router as employee_router
from user import router as user_router
print(Schemas.__file__)
# print(UserRegister.model_json_schema())
from Schemas import UserRegister, UserLogin, ProductCreate, CartCreate, CartUpdate, Checkout,DeleteCart
from fastapi import Depends
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

from fastapi import FastAPI
import uvicorn
from database import engine
from models import Base, Product, User,Cart


Base.metadata.create_all(bind=engine)
from database import SessionLocal
from models import Base, Product, User,Order
from Schemas import Checkout
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    description="FastAPI E-Commerce Backend with JWT Authentication"
    
)

app.include_router(employee_router)
app.include_router(user_router)
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):

    token = credentials.credentials

    email = verify_token(token)

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    db.close()

    return user

from fastapi import Depends, HTTPException

def employee_only(current_user: User = Depends(get_current_user)):

    if current_user.role != "employee":
        raise HTTPException(
            status_code=403,
            detail="Only employees can access this API."
        )

    return current_user

def user_only(current_user: User = Depends(get_current_user)):

    if current_user.role != "user":
        raise HTTPException(
            status_code=403,
            detail="Only users can access this API."
        )

    return current_user

@app.post("/register", tags=["Authentication"])
def register(user: UserRegister):

    db = SessionLocal()

    # Check if user already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        db.close()
        return {"message": "User already exists"}

    new_user = User(
    username=user.username,
    email=user.email,
    password=hash_password(user.password),
    role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "message": "User Registered Successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }

@app.post("/login",tags=["Authentication"])
def login(user: UserLogin):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        db.close()
        return {"message": "Invalid Email"}

    if not verify_password(user.password, existing_user.password):
        db.close()
        return {"message": "Invalid Password"}

    db.close()

    token = create_access_token(
    {
        "sub": existing_user.email,
        "role": existing_user.role
    })
    return {
    "access_token": token,
    "token_type": "Bearer"
}

@app.get("/products", tags=["Products"])
def get_products(
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    products = db.query(Product).all()

    db.close()

    return {
        "logged_in_user": current_user.email,
        "role": current_user.role,
        "products": products
    }

def main():

    uvicorn.run(
        "test:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()