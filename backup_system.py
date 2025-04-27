import os  # Работа с файловой системой
import shutil  # Копирование файлов и папок
import hashlib  # Хеширование данных для проверки целостности
import datetime  # Работа с датами и временем


class BackupSystem:
    def __init__(self, source_dir, backup_dir):
        """Инициализация системы резервного копирования."""
        self.source_dir = source_dir  # Папка с исходными данными
        self.backup_dir = backup_dir  # Папка для хранения резервных копий
        if not os.path.exists(self.backup_dir):  # Проверяем, существует ли папка
            os.makedirs(self.backup_dir)  # Создаем папку резервных копий

    def create_backup(self):
        """Создание резервной копии с меткой времени."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Форматируем текущую дату
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")  # Путь к новой резервной копии
        shutil.copytree(self.source_dir, backup_path)  # Копируем все файлы и папки
        print(f"Backup created at {backup_path}")  # Выводим сообщение о создании
        return backup_path  # Возвращаем путь к резервной копии

    def restore_backup(self, backup_path):
        """Восстановление данных из резервной копии."""
        if os.path.exists(backup_path):  # Проверяем, существует ли резервная копия
            shutil.rmtree(self.source_dir)  # Удаляем текущую папку с данными
            shutil.copytree(backup_path, self.source_dir)  # Восстанавливаем файлы
            print(f"Backup restored from {backup_path}")  # Выводим сообщение о восстановлении
        else:
            print("Backup path does not exist.")  # Сообщение об ошибке, если копия отсутствует

    def calculate_hash(self, directory):
        """Вычисление хеш-сумм файлов в указанной директории."""
        file_hashes = {}  # Словарь для хранения хешей файлов
        for root, _, files in os.walk(directory):  # Обход всех файлов в папке
            for file in files:
                file_path = os.path.join(root, file)  # Полный путь к файлу
                hasher = hashlib.sha256()  # Используем SHA-256 для хеширования
                with open(file_path, 'rb') as f:
                    buf = f.read()  # Читаем содержимое файла
                    hasher.update(buf)  # Обновляем хеш-сумму
                file_hashes[file_path] = hasher.hexdigest()  # Сохраняем хеш в словарь
        return file_hashes  # Возвращаем словарь с хешами

    def verify_backup_integrity(self, backup_path):
        """Сравнение хеш-сумм исходных и резервных данных для проверки целостности."""
        original_hashes = self.calculate_hash(self.source_dir)  # Хеши исходных данных
        backup_hashes = self.calculate_hash(backup_path)  # Хеши резервной копии

        if original_hashes == backup_hashes:  # Сравниваем хеши
            print("Backup integrity verified: Data is identical.")  # Сообщение об успешной проверке
        else:
            print("Backup integrity failed: Differences detected.")  # Сообщение об ошибке


# Действия для запуска кода в PyCharm:
# 1. Открыть PyCharm и создать новый проект.
# 2. Создать директории 'data_source' (исходные данные) и 'data_backup' (резервные копии).
# 3. Добавить несколько файлов в 'data_source' для тестирования.
# 4. Создать новый файл 'backup_system.py' и вставить в него этот код.
# 5. Запустить скрипт и проверить вывод.

# Пример использования
source_directory = "data_source"  # Папка с исходными данными
backup_directory = "data_backup"  # Папка для резервных копий

# Создаем систему резервирования
backup_system = BackupSystem(source_directory, backup_directory)

# Создаем резервную копию
backup_path = backup_system.create_backup()

# Проверяем целостность
backup_system.verify_backup_integrity(backup_path)

# Восстанавливаем данные
backup_system.restore_backup(backup_path)
