# FastAPI Orders Service

## Описание
FastAPI Orders Service — это асинхронный сервис управления заказами, построенный на FastAPI, PostgreSQL и RabbitMQ.

## Возможности
- Регистрация и аутентификация пользователей (OAuth2 с JWT)
- Создание, редактирование и удаление заказов
- Получение списка заказов с фильтрацией по статусу
- Взаимодействие с PostgreSQL через SQLAlchemy
- Асинхронные очереди сообщений с RabbitMQ
- Кеширование с использованием Redis
- Развёртывание через Docker Compose
- Автоматическая документация API (Swagger UI)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/fastapi_orders.git
cd fastapi_orders
```

### 2. Запуск через Docker Compose
```bash
docker-compose up --build -d
```

### 3. Проверка работы API
Документация API доступна по адресу:
```
http://localhost:8000/docs
```

## Остановка сервиса
```bash
docker-compose down -v
```

## Переменные окружения
Перед запуском убедитесь, что у вас настроены переменные окружения (можно задать их в `.env`):
```
DATABASE_URL=postgresql+asyncpg://user:password@postgres_db:5432/orders_db
RABBITMQ_URL=amqp://guest:guest@rabbitmq/
REDIS_URL=redis://redis_cache:6379/0
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Разработка и тестирование
### Локальный запуск без Docker
Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

Запустите приложение:
```bash
uvicorn app.main:app --reload
```

### Запуск тестов
```bash
pytest
```

## Развёртывание на сервере
1. Соберите образ Docker и отправьте его в реестр (Docker Hub, GitHub Container Registry и т. д.).
2. Настройте `.env` на сервере.
3. Используйте `docker-compose up -d` для развёртывания.

## Лицензия
MIT License

