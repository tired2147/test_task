import PyInstaller.__main__
import os
import shutil

def build_server():
    
    # Очищаем предыдущие сборки
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    PyInstaller.__main__.run([
        'app.py',
        '--name=ClickDataServer',
        '--onedir', # сервер в папке
        '--add-data=requirements.txt;.',
        '--hidden-import=sqlalchemy.ext.declarative',
        '--hidden-import=sqlalchemy.orm',
        '--hidden-import=pydantic',
        '--hidden-import=uvicorn',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.loops',
        '--hidden-import=uvicorn.protocols',
        '--clean',
        '--noconfirm'
    ])
    
    print("Сервер собран в: server/dist/ClickDataServer/")

if __name__ == "__main__":
    build_server()