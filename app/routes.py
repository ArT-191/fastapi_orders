from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import json
import logging
from app.auth import authenticate_user, get_current_user
from app.models import Order, User
from app.schemas import OrderCreate, OrderUpdate, OrderResponse, UserCreate
from app.services import create_order_service, get_order_service, update_order_service, get_user_orders_service, create_user_service, create_access_token
from app.database import get_db
from app.redis import redis_client


router = APIRouter()

# Логирование
logger = logging.getLogger(__name__)

@router.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    await create_user_service(user, db)
    return {"message": "User created successfully"}

@router.post("/token/")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)  # используем form_data.username
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Генерация и возвращение JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/orders/", response_model=List[OrderResponse]) 
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"Current user: {current_user}")  # Добавьте вывод в консоль
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.post("/orders/")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)  # Обновление заказа после добавления
    return db_order  # Вернем объект с id

@router.get("/orders/{order_id}/", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    cache_key = f"order:{order_id}"
    cached_order = redis_client.get(cache_key)
    if cached_order:
        return json.loads(cached_order)
    
    order = get_order_service(order_id, db)
    if order.user_id != current_user.id:  # Исправлено обращение к атрибуту через точку
        raise HTTPException(status_code=403, detail="Forbidden")
    redis_client.setex(cache_key, 300, json.dumps(order.dict()))  # Сериализация в строку
    return order

@router.patch("/orders/{order_id}/", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if not order_update.status:
        raise HTTPException(status_code=400, detail="Only status update is allowed")
    
    updated_order = update_order_service(order_id, order_update, db)
    if updated_order.user_id != current_user['user_id']:
        raise HTTPException(status_code=403, detail="Forbidden")
    cache_key = f"order:{order_id}"
    redis_client.delete(cache_key)  # Удаляем старый кеш
    return updated_order

@router.get("/orders/user/{user_id}/", response_model=List[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if user_id != current_user['user_id']:
        raise HTTPException(status_code=403, detail="Forbidden")
    orders = get_user_orders_service(user_id, db)
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders
