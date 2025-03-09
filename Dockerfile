# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем зависимости
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Запуск сервера Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

