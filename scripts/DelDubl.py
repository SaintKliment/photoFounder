import os
import hashlib
from PIL import Image

def calculate_image_hash(image_path):
    """Рассчитывает хэш изображения по его содержимому."""
    with Image.open(image_path) as img:
        # Преобразуем изображение в байты
        img_bytes = img.tobytes()
        # Вычисляем хэш MD5
        img_hash = hashlib.md5(img_bytes).hexdigest()
    return img_hash

def remove_duplicate_images(folder_path):
    """Удаляет дубликаты изображений, оставляя только уникальные."""
    # Словарь для хранения уникальных хэшей
    hashes = {}
    # Проходим по всем файлам в папке
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Пробуем открыть только изображения
            try:
                img_hash = calculate_image_hash(file_path)
                if img_hash in hashes:
                    # Если хэш уже существует, удаляем дубликат
                    print(f"Удаление дубликата: {file_path}")
                    os.remove(file_path)
                else:
                    # Добавляем новый уникальный хэш
                    hashes[img_hash] = file_path
            except Exception as e:
                print(f"Не удалось обработать файл {file_path}: {e}")

# Пример использования
folder_with_images = './primary_photos'
remove_duplicate_images(folder_with_images)
