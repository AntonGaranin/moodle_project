from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Загружаем существующие переменные из .env файла
load_dotenv()

if "ENCRYPTION_KEY" not in os.environ:
    key = Fernet.generate_key().decode()

    # Записываем в .env файл
    with open('.env', 'a') as f:
        f.write(f'\nENCRYPTION_KEY={key}\n')

    # Обновляем текущее окружение
    os.environ['ENCRYPTION_KEY'] = key
    print(f"Ключ сохранён в .env файл: {key}")
else:
    print(f"Используется существующий ключ: {os.environ['ENCRYPTION_KEY']}")