# Импортируем необходимые компоненты из SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


# declarative_base()-базовый класс для всех моделеей
Base = declarative_base()

class ClickData(Base):

    
    __tablename__ = "click_data"
    
    
    id = Column(Integer, primary_key=True, index=True)
    
    text = Column(String, index=True)
    
    click_count = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.now)