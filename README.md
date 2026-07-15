# 🛒 E-Commerce Backend API using FastAPI

This project is a RESTful E-Commerce Backend API developed using **FastAPI** and **SQLAlchemy**. It provides secure user authentication using **JWT Bearer Tokens**, product management, shopping cart functionality, and order checkout.

The application follows REST API best practices and demonstrates complete backend development with authentication, database integration, and CRUD operations.

## 🚀 Features

- User Registration
- User Login
- JWT Bearer Authentication
- Password Hashing using Passlib & Bcrypt
- Product Management (Add, View)
- Shopping Cart (Add, View, Update, Delete)
- Secure Checkout with Bill Generation
- SQLite/PostgreSQL Database Support
- SQLAlchemy ORM
- Interactive Swagger API Documentation

## 🛠️ Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- JWT Authentication
- Passlib (Bcrypt)
- Uvicorn
- Pydantic

## 📌 API Modules

- Authentication
- Products
- Shopping Cart
- Checkout

## 🔐 Security

- Passwords are securely hashed using Bcrypt.
- JWT Bearer Token authentication protects secured endpoints.
- Only authenticated users can access cart and checkout operations.

## 📈 Future Enhancements

- Role-Based Access Control (Admin & Customer)
- Product Search & Filtering
- Pagination
- Image Upload
- Payment Gateway Integration
- Docker Deployment
- CI/CD Pipeline
