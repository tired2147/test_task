import pytest
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QStringListModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from client.client_app import ClickDataClient

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
#ТЕСТ 1: отправка данных на сервер
def test_send_data_success(qapp):
    
    client = ClickDataClient()
    client.input_field.setText("Test message")
    
    with patch('client.client_app.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1, 
            "text": "Test message", 
            "click_count": 1,
            "created_at": "2024-01-01T12:00:00.000000"
        }
        mock_post.return_value = mock_response
        
        client.send_data()
        
        assert client.click_count == 1
        assert client.click_count_label.text() == "Отправлено кликов: 1"
        mock_post.assert_called_once_with(
            "http://localhost:8000/api/clicks/",
            json={"text": "Test message", "click_count": 1},
            timeout=10
        )
#ТЕСТ 2: получение данных
def test_get_data_success(qapp):
    
    client = ClickDataClient()
    
    mock_data = {
        "items": [
            {
                "id": 1,
                "text": "Test message 1",
                "click_count": 1,
                "created_at": "2024-01-01T12:00:00.000000"
            }
        ],
        "total": 1,
        "page": 1,
        "size": 20,
        "pages": 1
    }
    
    with patch('client.client_app.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        client.get_data()
        
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/click-history/?page=1&size=20",
            timeout=10
        )
        
        #  данные отобразились в интерфейсе
        assert len(client.list_model.stringList()) == 1
        assert "Test message 1" in client.list_model.stringList()[0]
#ТЕСТ 3: Обработка ошибки соединения при отправке данных
def test_send_data_connection_error(qapp):
    client = ClickDataClient()
    client.input_field.setText("Test message")
    
    with patch('client.client_app.requests.post') as mock_post:
        mock_post.side_effect = ConnectionError("Connection failed")
        
        client.send_data()
        
        #   статус обновился с информацией об ошибке
        assert "Не удалось подключиться к серверу" in client.status_label.text()
        # Счетчик увеличился, тк попытка была
        assert client.click_count == 1