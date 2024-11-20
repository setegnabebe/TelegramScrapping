# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'  # Name of the table

    id = Column(Integer, primary_key=True, index=True)  
    date = Column(DateTime, nullable=False)  
    message = Column(Text, nullable=True)  
    media = Column(String, nullable=True)  
