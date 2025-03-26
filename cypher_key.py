from cryptography.fernet import Fernet
import os

# Проверяем, есть ли переменная окружения
if "ENCRYPTION_KEY" not in os.environ:
    key = Fernet.generate_key().decode()  # Декодируем байты в строку
    os.environ["ENCRYPTION_KEY"] = key  # Устанавливаем переменную окружения
    print(f"Создана переменная окружения ENCRYPTION_KEY: {key}")
else:
    print("Переменная ENCRYPTION_KEY уже существует.")