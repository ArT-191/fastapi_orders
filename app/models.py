from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")  # Связь с Order


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")
    items = Column(JSON, nullable=False)  # Используем тип JSON для PostgreSQL
    user_id = Column(Integer, ForeignKey("users.id"))  # Внешний ключ
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="orders")