import sys
import requests
from datetime import datetime
from typing import List, Dict, Any
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLineEdit, QListView, QPushButton, 
    QMessageBox, QLabel, QFrame
)
from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtGui import QFont

class ClickDataClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.server_url = "http://localhost:8000"
        self.init_ui()
        self.set_styles()
        
    def init_ui(self):
        self.setWindowTitle("Click Data Client")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title_label = QLabel("Приложение для работы с сервером")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("title")
        main_layout.addWidget(title_label)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        #Инпуты
        input_layout = QVBoxLayout()
        
        input_label = QLabel("Введите текст для отправки:")
        input_label.setObjectName("section_label")
        input_layout.addWidget(input_label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите текст здесь...")
        self.input_field.setMinimumHeight(40)
        self.input_field.setObjectName("input_field")
        input_layout.addWidget(self.input_field)
        
        main_layout.addLayout(input_layout)
        
        #Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.send_button = QPushButton("Отправить данные")
        self.send_button.setMinimumHeight(45)
        self.send_button.setObjectName("send_button")
        self.send_button.clicked.connect(self.send_data)
        buttons_layout.addWidget(self.send_button)
        
        self.get_button = QPushButton("Получить данные")
        self.get_button.setMinimumHeight(45)
        self.get_button.setObjectName("get_button")
        self.get_button.clicked.connect(self.get_data)
        buttons_layout.addWidget(self.get_button)
        
        main_layout.addLayout(buttons_layout)
        
        #Инфа по запросам
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Готов к работе")
        self.status_label.setObjectName("status_label")
        status_layout.addWidget(self.status_label)
        
        self.click_count_label = QLabel(f"Порядковый номер клика: {self.click_count}")
        self.click_count_label.setObjectName("count_label")
        status_layout.addWidget(self.click_count_label)
        
        main_layout.addLayout(status_layout)
        
        #Виджет для полученного текста
        data_layout = QVBoxLayout()
        
        data_label = QLabel("Полученные данные с сервера:")
        data_label.setObjectName("section_label")
        data_layout.addWidget(data_label)
        
        self.list_view = QListView()
        self.list_view.setMinimumHeight(300)
        self.list_view.setObjectName("list_view")
        self.list_model = QStringListModel()
        self.list_view.setModel(self.list_model)
        data_layout.addWidget(self.list_view)
        
        main_layout.addLayout(data_layout)
        
        central_widget.setLayout(main_layout)
        
    def set_styles(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            #title {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            #section_label {
                font-size: 14px;
                font-weight: bold;
                color: #34495e;
            }
            #input_field {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                color: #2c3e50;
            }
            #input_field:focus {
                border-color: #3498db;
            }
            #input_field::placeholder {
            color: #95a5a6;  /* Цвет placeholder текста */
            }
            #send_button {
                font-size: 14px;
                font-weight: bold;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            #send_button:hover {
                background-color: #229954;
            }
            #send_button:pressed {
                background-color: #1e8449;
            }
            #get_button {
                font-size: 14px;
                font-weight: bold;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            #get_button:hover {
                background-color: #2980b9;
            }
            #get_button:pressed {
                background-color: #2471a3;
            }
            #status_label {
                font-size: 12px;
                color: #7f8c8d;
                padding: 5px;
                background-color: transparent;
            }
            #count_label {
                font-size: 12px;
                color: #e74c3c;
                font-weight: bold;
                padding: 5px;
                background-color: transparent;
            }
            #list_view {
                font-size: 12px;
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                color: #2c3e50;
            }
            QListView::item {
                padding: 5px;
                border-bottom: 1px solid #ecf0f1;
                color: #2c3e50;
                background-color: white;
            }
            QListView::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
            QLabel {
            color: #2c3e50;  /* Общий цвет текста для всех QLabel */
            background-color: transparent;
        """)
        
    def update_status(self, message: str, is_error: bool = False):
        #Обновление статуса строки
        color = "#e74c3c" if is_error else "#27ae60"
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color};")
        
    def send_data(self):
        #Отправка данных на сервер
        try:
            text = self.input_field.text().strip()
            if not text:
                self.update_status("Ошибка: Введите текст перед отправкой", True)
                QMessageBox.warning(self, "Ошибка", "Введите текст перед отправкой")
                return
            
            self.click_count += 1
            self.click_count_label.setText(f"Отправлено кликов: {self.click_count}")
            
            data = {
                "text": text,
                "click_count": self.click_count
            }
            
            self.update_status("Отправка данных...")
            
            response = requests.post(
                f"{self.server_url}/api/clicks/",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status("Данные успешно отправлены!")
                self.input_field.clear()
                QMessageBox.information(self, "Успешно", "Данные успешно отправлены на сервер")
            else:
                self.update_status(f"Ошибка сервера: {response.status_code}", True)
                QMessageBox.critical(self, "Ошибка", 
                    f"Ошибка сервера: {response.status_code}\n{response.text}")
                
        except requests.exceptions.ConnectionError:
            self.update_status("Ошибка: Не удалось подключиться к серверу", True)
            QMessageBox.critical(self, "Ошибка", 
                "Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
        except requests.exceptions.Timeout:
            self.update_status("Ошибка: Таймаут соединения", True)
            QMessageBox.critical(self, "Ошибка", "Таймаут соединения с сервером")
        except Exception as e:
            self.update_status(f"Неизвестная ошибка: {str(e)}", True)
            QMessageBox.critical(self, "Ошибка", f"Неизвестная ошибка: {str(e)}")
    
    def get_data(self):
        #Получение данных с сервера
        try:
            self.update_status("Получение данных...")
            
            response = requests.get(
                f"{self.server_url}/api/click-history/?page=1&size=20",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                #total = data.get('total', int)
                display_data = []
                #display_data.append(f"Всего записей: {total}")
                for item in items:
                    text = item.get('text', '')
                    click_count = item.get('click_count', 0)
                    created_at = item.get('created_at', '')
                    
                    # Парсим дату и время
                    if created_at:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        date_str = dt.strftime("%Y-%m-%d")
                        time_str = dt.strftime("%H:%M:%S")
                        display_data.append(
                            f"Дата время: {date_str} {time_str} - Текст: {text}, Номер клика: {click_count}"
                        )
                    else:
                        display_data.append(f"Текст: {text}, Номер клика: {click_count}")
                
                self.list_model.setStringList(display_data)
                self.update_status(f"Получено {len(display_data)} записей")
                
            else:
                self.update_status(f"Ошибка сервера: {response.status_code}", True)
                QMessageBox.critical(self, "Ошибка", 
                    f"Ошибка сервера: {response.status_code}\n{response.text}")
                
        except requests.exceptions.ConnectionError:
            self.update_status("Ошибка: Не удалось подключиться к серверу", True)
            QMessageBox.critical(self, "Ошибка", 
                "Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
        except requests.exceptions.Timeout:
            self.update_status("Ошибка: Таймаут соединения", True)
            QMessageBox.critical(self, "Ошибка", "Таймаут соединения с сервером")
        except Exception as e:
            self.update_status(f"Неизвестная ошибка: {str(e)}", True)
            QMessageBox.critical(self, "Ошибка", f"Неизвестная ошибка: {str(e)}")

def main():
    
    app = QApplication(sys.argv)
    
    #  стиль приложения
    app.setStyle('Fusion')
    
    client = ClickDataClient()
    client.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()