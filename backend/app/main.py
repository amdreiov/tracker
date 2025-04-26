from fastapi import FastAPI, Request, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models

# Создание таблиц БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["tracker.amdrei.ru", "localhost"]
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Инициализация шаблонов
templates = Jinja2Templates(directory="frontend/templates")

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "ok", "db": "connected"}