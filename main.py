# main.py
# Головний файл, який приймає запити з сайту

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Підключаємо наші оновлені моделі та налаштування бази
import models
from database import SessionLocal, engine, Base

# Ця команда створює в базі даних таблицю "inquiries" за нашим кресленням
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Шаблони для даних ---

# Шаблон для даних, які приходять з сайту
class InquiryCreate(BaseModel):
    name: str
    email: str
    message: str

# Шаблон для даних, які ми віддаємо у відповідь
class InquiryResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str

    class Config:
        orm_mode = True

# --- Функції для роботи з базою ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- "Двері" на нашу кухню (Ендпоінти) ---

# Головна сторінка API (можна залишити для перевірки)
@app.get("/")
def read_root():
    return {"message": "API для сайту pikitodoritos працює!"}

# Нові двері для ПРИЙОМУ заявок з контактної форми
# Адреса буде /inquiries/, метод POST
@app.post("/inquiries/", response_model=InquiryResponse)
def create_inquiry(inquiry: InquiryCreate, db: Session = Depends(get_db)):
    # Створюємо запис в базі за кресленням ClientInquiry
    db_inquiry = models.ClientInquiry(
        name=inquiry.name, email=inquiry.email, message=inquiry.message
    )
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

# Двері, щоб ПЕРЕГЛЯНУТИ всі заявки, які надійшли
# Адреса буде /inquiries/, метод GET
@app.get("/inquiries/", response_model=List[InquiryResponse])
def read_inquiries(db: Session = Depends(get_db)):
    inquiries = db.query(models.ClientInquiry).all()
    return inquiries