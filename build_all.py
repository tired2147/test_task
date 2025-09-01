
import os
import subprocess
import sys

def build_all():
    
    
    # Сборка сервера
    print("\nСборка сервера...")
    os.chdir('server')
    result = subprocess.run([sys.executable, 'build.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Ошибки сервера:", result.stderr)
    os.chdir('..')
    
    # Сборка клиента
    print("\nСборка клиента...")
    os.chdir('client')
    result = subprocess.run([sys.executable, 'build.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Ошибки клиента:", result.stderr)
    os.chdir('..')
    
    print("\n🎉 Сборка завершена!")

if __name__ == "__main__":
    build_all()