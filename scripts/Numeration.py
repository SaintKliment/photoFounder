import os

def rename_files_in_directory(directory, start_index=1):
    # Получаем список всех файлов в папке
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Сортируем файлы по имени, чтобы они шли в определенном порядке
    files.sort()
    
    # Переименовываем файлы в формате img_{start_index}, img_{start_index+1}, ..., img_{start_index+N}
    for i, filename in enumerate(files, start=start_index):
        # Получаем расширение файла
        file_extension = os.path.splitext(filename)[1]
        
        # Создаем новое имя файла
        new_name = f"image_{i}{file_extension}"
        
        # Полные пути для оригинального и нового имени
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        # Переименовываем файл
        os.rename(old_path, new_path)
        print(f"Переименован: {filename} -> {new_name}")

# Укажите путь к вашей папке и начальный индекс
folder_path = './filters_photos'
start_index = 1  # Например, начинаем с 100

# Запуск функции переименования
rename_files_in_directory(folder_path, start_index)
