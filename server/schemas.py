from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date as date_type, time as time_type
from typing import List

class ClickDataBase(BaseModel):
    #Базовая схема для данных
    text: str = Field(..., min_length=1, description="Текст из QLineEdit")
    click_count: int = Field(..., ge=1, description="Порядковый номер клика")

class ClickDataCreate(ClickDataBase):
    #Схема для создания новой записи
    pass

class ClickData(ClickDataBase):
    #Полная схема данных 
    id: int = Field(..., description="Уникальный идентификатор записи")
    created_at: datetime = Field(..., description="Полная временная метка создания")
    
    # для даты и времени
    @property
    def date(self) -> date_type:
        
        return self.created_at.date()
    
    @property
    def time(self) -> time_type:
        
        return self.created_at.time()

    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel):
    #Схема для ответа с пагинации
    items: List[ClickData] = Field(..., description="Список записей на текущей странице")
    total: int = Field(..., ge=0, description="Общее количество записей")
    page: int = Field(..., ge=1, description="Текущая страница")
    size: int = Field(..., ge=1, le=100, description="Количество записей на странице")
    pages: int = Field(..., ge=0, description="Общее количество страниц")