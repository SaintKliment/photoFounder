import os
from PIL import Image
import time

# Путь к папке с изображениями
folder_path = './workspace_photos/primary_photos'

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Проверяем, является ли файл изображением
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif')):
        print(f"Пропущен не изображение: {filename}")
        continue
    
    try:
        # Открываем изображение
        with Image.open(file_path) as img:
            img.verify()  # Проверка целостности файла изображения
            width, height = img.size
            
            # Проверяем размер изображения
            if width < 500 or height < 500:
                # time.sleep(1)  # Задержка в 1 секунду
                # Удаляем изображение, если его размер <= 500x500
                os.remove(file_path)
                print(f"Удалено: {filename} (Размер: {width}x{height})")
            else:
                print(f"Оставлено: {filename} (Размер: {width}x{height})")

    except (IOError, SyntaxError) as e:
        # Удаляем файл, если возникла ошибка открытия или проверка изображения не прошла
        print(f"Ошибка при открытии {filename}, удаление файла: {e}")
        os.remove(file_path)
