import logging
import os
from logging.handlers import RotatingFileHandler

# Проверка на существовние директории или ее создание
if not os.path.exists("logs"):
    os.makedirs("logs")

# Нвстройка логгера
logger = logging.getLogger("celery")
logger.setLevel(logging.INFO)

# Настройка обработчика с ротацией файлов (макс. 10 МБ, сохраняем 5 резервных копий)
handler = RotatingFileHandler("logs/app.log", maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Добавление обработчика в логгер
logger.addHandler(handler)
