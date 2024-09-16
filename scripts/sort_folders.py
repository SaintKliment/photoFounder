import os
import shutil

def distribute_files(source_folder, dest_folder, files_per_folder=1000):
    # Получаем список всех файлов в исходной папке
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    # Счетчик для номеров папок
    folder_count = 15
    file_count = 0

    # Создаем папки и перемещаем файлы
    for i, file_name in enumerate(files):
        # Если file_count достигает files_per_folder, создаем новую папку
        if file_count % files_per_folder == 0:
            folder_count += 1
            new_folder = os.path.join(dest_folder, f'part_{folder_count}')
            os.makedirs(new_folder, exist_ok=True)

        # Полные пути к исходному и новому файлу
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(new_folder, file_name)
        
        # Перемещаем файл в новую папку
        shutil.move(source_file, destination_file)
        
        # Увеличиваем счетчик файлов
        file_count += 1

    print(f"Все файлы успешно распределены по папкам в {dest_folder}")

# Параметры
source_folder = './filters_photos'  # Путь к папке с исходными файлами
dest_folder = './destination_folder'  # Путь к папке для распределенных файлов

# Запуск функции
distribute_files(source_folder, dest_folder)
