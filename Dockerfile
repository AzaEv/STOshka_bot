# Используем легкий образ Python
FROM python:3.9-slim

# Устанавливаем рабочую папку
WORKDIR /app

# Копируем список библиотек и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Команда запуска
CMD ["python", "app.py"]
