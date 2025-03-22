from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class OrderItem(BaseModel):  
    name: str
    qty: int    

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    status: Optional[str] = None
    items: Optional[List[OrderItem]] = None  

class OrderCreate(BaseModel):
    customer_name: str
    total_price: float
    status: str
    items: List[OrderItem]  
    user_id: int

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    items: List[OrderItem]  
    created_at: datetime

    class Config:
        orm_mode = True  # Используется для работы с SQLAlchemy, чтобы преобразовать ORM-объекты в Pydantic модели

class UserCreate(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
