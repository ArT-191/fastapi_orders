from app.models import Order, User
from app.schemas import OrderCreate, OrderUpdate, UserCreate
from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import json
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils import hash_password, verify_password

def create_order_service(order: OrderCreate, db: Session):
    # Сериализация 'items' в строку JSON
    items_json = json.dumps([item.dict() for item in order.items])  # Преобразуем список объектов в JSON

    # Создаем объект заказа для базы данных
    order_in_db = Order(
        customer_name=order.customer_name,
        total_price=order.total_price,
        status=order.status,
        items=items_json,  # Сохраняем items как строку JSON
        user_id=order.user_id
    )

    # Добавляем в базу данных и сохраняем изменения
    db.add(order_in_db)
    db.commit()
    db.refresh(order_in_db)  # Обновляем объект с новыми данными

    # Возвращаем заказ, включая id, который был автоматически присвоен
    return order_in_db

def get_order_service(order_id, db):
    order = db.query(Order).filter(Order.id == order_id).first()
    return order 

def update_order_service(order_id: str, order: OrderUpdate, db: Session):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order

# Функция для получения всех заказов пользователя
def get_user_orders_service(user_id: str, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()

# Ваш секретный ключ для создания JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])



async def create_user_service(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    new_user = User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()  # <-- Используем email вместо username
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
