from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Product, Cart, Order

# SQLite
sqlite_engine = create_engine("sqlite:///./ecommerce.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)

# PostgreSQL
postgres_engine = create_engine(
    "postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce"
)
PostgresSession = sessionmaker(bind=postgres_engine)

sqlite_db = SQLiteSession()
postgres_db = PostgresSession()

# Users
for user in sqlite_db.query(User).all():
    postgres_db.add(
        User(
            id=user.id,
            email=user.email,
            password=user.password
        )
    )

# Products
for product in sqlite_db.query(Product).all():
    postgres_db.add(
        Product(
            id=product.id,
            name=product.name,
            price=product.price
        )
    )

# Cart
for cart in sqlite_db.query(Cart).all():
    postgres_db.add(
        Cart(
            id=cart.id,
            user_id=cart.user_id,
            product_id=cart.product_id,
            quantity=cart.quantity
        )
    )

# Orders
for order in sqlite_db.query(Order).all():
    postgres_db.add(
        Order(
            id=order.id,
            user_id=order.user_id,
            total_amount=order.total_amount,
            status=order.status
        )
    )

postgres_db.commit()

sqlite_db.close()
postgres_db.close()

print("Data migrated successfully!")