from django.core.management import BaseCommand
from main.tasks import scan_and_process_files


# Асинхронный способ
# class Command(BaseCommand):
#     help = "Запускает сканирование и обработку файлов"
#
#     def handle(self, *args, **options):
#         task = scan_and_process_files.delay()
#         self.stdout.write(self.style.SUCCESS(f"Запущена обработка файлов... Task ID: {task.id}"))


class Command(BaseCommand):
    help = "Запускает сканирование и обработку файлов"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Запуск сканирования и обработки файлов ..."))

        result_object = scan_and_process_files()

        if not result_object.get("success"):
            self.stdout.write(self.style.ERROR(result_object.get("message")))
        else:
            for result in result_object.get("results"):
                self.stdout.write(self.style.SUCCESS(result))

            self.stdout.write(self.style.SUCCESS("Завершено!"))
