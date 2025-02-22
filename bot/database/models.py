from sqlalchemy import Column, Integer, String, DateTime, func
from bot.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    last_active = Column(DateTime, default=func.now(), onupdate=func.now())  # Добавляем last_active
