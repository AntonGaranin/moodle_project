from cryptography.fernet import Fernet
import os

# Проверяем, есть ли уже ключ в переменных окружения
if "ENCRYPTION_KEY" not in os.environ:
    key = Fernet.generate_key()
    os.environ["ENCRYPTION_KEY"] = key.decode()  # Сохраняем как строку
    print("Ключ сгенерирован и сохранён в переменные окружения.")
else:
    print("Ключ уже существует, перегенерация не требуется.")