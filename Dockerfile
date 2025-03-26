# Используем официальный образ Python
FROM python:3.9-slim

# Установим зависимости для работы с Git и другими инструментами
RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG CACHEBUST=1

# Установим необходимые библиотеки Python
RUN pip install --no-cache-dir aiogram requests beautifulsoup4 lxml cryptography python-dotenv

# Клонируем ваш репозиторий через HTTPS
RUN git clone --branch actions_setting --single-branch https://github.com/AntonGaranin/moodle_project.git /app

# Укажем рабочую директорию
WORKDIR /app

# Команда для создания ключа шифрования
CMD ["python", "cypher_key.py"]

# Укажем команду для запуска бота
CMD ["python", "main.py"]
