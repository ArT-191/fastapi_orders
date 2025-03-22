from fastapi import FastAPI
from app.routes import router  # Убедись, что импорт соответствует тому, что есть в routes.py

app = FastAPI(debug=True)

# Подключение маршрутов
app.include_router(router)

@app.get("/")
def root():
    return {"message": "FastAPI Orders Service is running"}