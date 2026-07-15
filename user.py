from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, Product, Cart, Order
from Schemas import CartCreate, CartUpdate, DeleteCart
from security import verify_token

router = APIRouter()

security = HTTPBearer()


# -----------------------------
# Database
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Authorization
# -----------------------------
def user_only(
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

    if user.role != "user":
        raise HTTPException(
            status_code=403,
            detail="Only Users can access this API."
        )

    return user


# -----------------------------
# View Products
# -----------------------------
@router.get("/products", tags=["Products"])
def get_products(
    current_user: User = Depends(user_only),
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return {
        "logged_in_user": current_user.email,
        "products": products
    }


# -----------------------------
# Add to Cart
# -----------------------------
@router.post("/cart", tags=["Cart"])
def add_to_cart(
    cart: CartCreate,
    current_user: User = Depends(user_only)
):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == cart.product_id
    ).first()

    if not product:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    new_cart = Cart(
        user_id=current_user.id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    db.close()

    return {
        "message": "Added to Cart Successfully"
    }

# -----------------------------
# View Cart
# -----------------------------
@router.get("/cart", tags=["Cart"])
def view_cart(
    current_user: User = Depends(user_only)
):

    db = SessionLocal()

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).all()

    result = []

    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        result.append({
            "cart_id": item.id,
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity
        })

    db.close()

    return result

# -----------------------------
# Update Cart
# -----------------------------
@router.put("/cart/{cart_id}", tags=["Cart"])
def update_cart(
    cart_id: int,
    cart: CartUpdate,
    current_user: User = Depends(user_only)
):

    db = SessionLocal()

    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Cart Item Not Found"
        )

    cart_item.quantity = cart.quantity

    db.commit()
    db.refresh(cart_item)

    db.close()

    return {
        "message": "Cart Updated Successfully"
    }

# -----------------------------
# Delete Cart
# -----------------------------
@router.delete("/cart/{cart_id}", tags=["Cart"])
def delete_cart(
    cart_id: int,
    current_user: User = Depends(user_only)
):

    db = SessionLocal()

    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Cart Item Not Found"
        )

    db.delete(cart_item)

    db.commit()

    db.close()

    return {
        "message": "Cart Deleted Successfully"
    }
# -----------------------------
# Checkout
# -----------------------------
@router.post("/checkout", tags=["Checkout"])
def checkout(
    current_user: User = Depends(user_only)
):

    db = SessionLocal()

    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).all()

    if not cart_items:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Cart is Empty"
        )

    total_amount = 0
    bill_items = []

    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        subtotal = product.price * item.quantity

        total_amount += subtotal

        bill_items.append({
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="Placed"
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    
    order_id = order.id
    status = order.status

    for item in cart_items:
        db.delete(item)
        db.commit()
        db.close()
        return {
        "message": "Order Placed Successfully",
        "order_id": order_id,
        "customer": current_user.email,
        "status": status,
        "items": bill_items,
        "total_amount": total_amount
}