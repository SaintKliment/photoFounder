import os
from PIL import Image

# Укажите путь к папке
folder_path = './workspace_photos/primary_photos' # primary_photos

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Проверяем, является ли файл изображением
    if os.path.isfile(file_path):
        try:
            # Открываем изображение
            with Image.open(file_path) as img:
                # Создаем новый путь с префиксом и расширением .jpg
                new_file_path = os.path.join(folder_path, f'conv_{os.path.splitext(filename)[0]}.jpg')
                # Сохраняем изображение в формате .jpg
                img.convert('RGB').save(new_file_path, 'JPEG')
                
                # Удаляем оригинальный файл (если нужно)
                os.remove(file_path)

                print(f'Преобразован: {file_path} -> {new_file_path}')
        except Exception as e:
            print(f'Ошибка обработки файла {file_path}: {e}')
