
import PyInstaller.__main__
import os
import shutil

def build_client():
    
    
    # Очищаем предыдущие сборки
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    PyInstaller.__main__.run([
        'client_app.py',
        '--name=ClickDataClient',
        '--onefile',        #  в одном файле
        '--windowed',       # Без консольного окна
        '--add-data=requirements.txt;.',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=requests',
        #'--icon=../assets/icon.ico',  
        '--clean',
        '--noconfirm'
    ])
    
    print("Клиент собран в: client/dist/ClickDataClient.exe")

if __name__ == "__main__":
    build_client()