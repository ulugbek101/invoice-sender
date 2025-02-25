import os
import requests

from django.conf import settings
from celery import shared_task
from config.logging_config import logger


@shared_task(bind=True, autoretry_for=(requests.RequestException,), retry_kwargs={"max_retries": 3, "countdown": 5})
def send_file_to_api(self, file_path):
    """
    Отправляет файл на внешний API через POST-запрос.
    Сохраняет ответ в DOWNLOAD_DIR, если запрос успешен.
    Если запрос не удался, задача будет повторяться до 3 раз.
    :param file_path: путь к файлу
    :return: Сообщение об успешной отправке или ошибке
    """

    logger.info(f"[TASK START] Отправка файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            error_message = f"Ошибка: Файл {file_path} не найден."
            logger.error(error_message)
            return error_message

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            response = requests.post(settings.API_URL, files=files, timeout=10)
            response.raise_for_status()

        os.makedirs(settings.DOWNLOAD_DIR, exist_ok=True)

        response_file_path = os.path.join(settings.DOWNLOAD_DIR, os.path.basename(file_path) + "_ответ.txt")

        with open(response_file_path, "w") as response_file:
            response_file.write(response.text)

        # os.remove(file_path)
        success_message = f"Файл {file_path} успешно отправлен. Ответ сохранен в {response_file_path}."
        logger.info(success_message)
        return success_message

    except requests.RequestException as e:
        error_message = f"Ошибка при отправке файла {file_path}: {e}"
        logger.error(error_message)
        raise

    finally:
        logger.info(f"[TASK END] Завершена обработка файла: {file_path}\n")


@shared_task()
def scan_and_process_files():
    """
    Сканирует директорию на наличие новых файлов и отправляет их в Celery задачу.
    Возвращает список результатов.
    """

    logger.info("Начало работы")
    if not os.path.exists(settings.UPLOAD_DIR):
        message = f"Директория {settings.UPLOAD_DIR} не существует"
        return {
            "success": False,
            "message": message,
        }

    files_found = [f for f in os.listdir(settings.UPLOAD_DIR) if os.path.isfile(os.path.join(settings.UPLOAD_DIR, f))]

    if not files_found:
        message = "Нет файлов для обработки в UPLOAD_DIR"
        return {
            "success": False,
            "message": message,
        }

    results = []

    for file_name in files_found:
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)
        task = send_file_to_api.delay(file_path)
        message = f"Файл {file_path} отправлен в очередь Celery. Task ID: {task.id}"
        logger.info(message)
        results.append(message)

    return {
        "success": True,
        "results": results,
    }
