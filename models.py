# models.py
# Ми описуємо, як буде виглядати заявка в нашій базі даних

from sqlalchemy import Column, Integer, String
from database import Base

class ClientInquiry(Base):
    __tablename__ = "inquiries" # Назва таблиці в базі буде "inquiries" (заявки)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # Поле для імені клієнта
    email = Column(String, index=True) # Поле для email
    message = Column(String) # Поле для повідомлення