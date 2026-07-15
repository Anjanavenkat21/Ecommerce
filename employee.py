from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, Product
from Schemas import ProductCreate
from security import verify_token

router = APIRouter(
    prefix="/employee",
    tags=["Products"]
)

security = HTTPBearer()


# Database Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authentication + Authorization
def employee_only(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    email = verify_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid User"
        )

    if user.role != "employee":
        raise HTTPException(
            status_code=403,
            detail="Access Denied! Only Employees can access this API."
        )

    return user


# -----------------------------
# Add Product
# -----------------------------
@router.post("/products", tags=["Products"])
def add_product(
    product: ProductCreate,
    current_user: User = Depends(employee_only),
    db: Session = Depends(get_db)
):

    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product Added Successfully",
        "added_by": current_user.email,
        "product": new_product
    }


# -----------------------------
# View Products


# -----------------------------
# Update Product
# -----------------------------
@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    current_user: User = Depends(employee_only),
    db: Session = Depends(get_db)
):

    db_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    db_product.name = product.name
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)

    return {
        "message": "Product Updated Successfully",
        "product": db_product
    }


# -----------------------------
# Delete Product
# -----------------------------
@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: User = Depends(employee_only),
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product Deleted Successfully"
    }