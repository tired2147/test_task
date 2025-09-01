"""
Точка входа для запуска FastAPI сервера.
"""
import uvicorn

if __name__ == "__main__":
    # Запускаем сервер с помощью uvicorn
    # app:app - модуль app, переменная app
    # reload=True - автоматическая перезагрузка при изменении кода
    # host="0.0.0.0" - слушаем все интерфейсы
    # port=8000 - порт по умолчанию
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )