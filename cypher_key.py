from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Загружаем существующие переменные из .env (если файл есть)
load_dotenv()

# Проверяем, есть ли уже ENCRYPTION_KEY
if os.getenv("ENCRYPTION_KEY") is None:
    # Генерируем новый ключ, если его нет
    key = Fernet.generate_key().decode()

    # Записываем ключ в .env
    with open(".env", "a") as f:
        f.write(f'ENCRYPTION_KEY="{key}"\n')

    # Перезагружаем переменные, чтобы новая переменная стала доступна
    load_dotenv()
    print("Новый ключ сгенерирован и сохранён в .env")
else:
    print("Ключ уже существует:", os.getenv("ENCRYPTION_KEY"))