# Импортируем FastAPI для создания API сервера
from fastapi import FastAPI, Depends, HTTPException, Query
# Импортируем Session для типизации сессии базы данных
from sqlalchemy.orm import Session
# Импортируем модуль logging для логирования
import logging
from datetime import datetime
# Импортируем наши модули
from server import models, schemas
from server.database import gget_db, create_tables

# Настраиваем логирование(INFO, DEBUG, WARNING, ERROR)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Test Task API")

@app.on_event("startup")
def on_startup():

    create_tables()
    logger.info("Таблицы базы данных созданы/проверены")

#только для Post запросов
@app.post("/api/clicks/", response_model=schemas.ClickData)
def create_click_data(
    click_data: schemas.ClickDataCreate,  # Данные из тела запроса (автом. валидируются)
    db: Session = Depends(gget_db)       
):

    try:
        
        now = datetime.now()
        
    
        db_click_data = models.ClickData(
            text=click_data.text,          # Текст из запроса
            click_count=click_data.click_count,  # Счетчик кликов из запроса
            created_at=now                 # Текущее время
        )
        
        db.add(db_click_data)
        db.commit()
        db.refresh(db_click_data)
        
        logger.info(f"Создана новая запись: ID={db_click_data.id}, текст='{click_data.text}'")
        
        # автоматически SQLAlchemy объект в Pydantic схему
        return db_click_data
        
    except Exception as e:
        # В случае ошибки откатываем транзакцию
        db.rollback()
        logger.error(f"Ошибка при создании записи: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

# только для get
@app.get("/api/click-history/", response_model=schemas.PaginatedResponse)
def get_click_data(
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество записей на странице (1-100)"),
    db: Session = Depends(gget_db)
):
   
    try:
        
        total = db.query(models.ClickData).count()
        
        # общее количество страниц
        pages = (total + size - 1) // size if total > 0 else 1
        
        # смещение для текущей страницы
        offset = (page - 1) * size
        
        #записи для текущей страницы
        items = db.query(models.ClickData).order_by(models.ClickData.created_at.desc()).offset(offset).limit(size).all()
        
        logger.info(f"Получено {len(items)} записей, страница {page}/{pages}")
        
        # Возвращаем данные в формате пагинации
        return schemas.PaginatedResponse(
            items=items,# Список записей
            total=total,  # Общее количество записей
            page=page,  # Текущая страница
            size=size,# Размер страницы
            pages=pages # Общее количество страниц
        )
        
    except Exception as e:
        logger.error(f"Ошибка при получении записей: {e}")
        
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@app.get("/health")
def health_check():
    
    return {"status": "ok", "message": "Сервер работает"}


#@app.api_route("/api/clicks/", methods=["GET", "PUT", "DELETE", "PATCH"], include_in_schema=False)
#def clicks_method_not_allowed():
    
 #   raise HTTPException(status_code=405, detail="Недопустимый метод для эндпоинта")

#@app.api_route("/api/click-history/", methods=["POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
#def click_history_method_not_allowed():
    
 #   raise HTTPException(status_code=405, detail="Недопустимый метод для эндпоинта")