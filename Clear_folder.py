import os
import shutil

def clear_folder(folder_path):
    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        print(f"Ошибка: Папка {folder_path} не существует.")
        return

    # Проходим по всем файлам и папкам в указанной папке
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        # Если это папка, удаляем её рекурсивно
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        # Если это файл, удаляем его
        elif os.path.isfile(item_path):
            os.remove(item_path)

    print(f"Папка {folder_path} успешно очищена.")

# Путь к папке, которую нужно очистить
folder_to_clear = './filters_photos'

# Очищаем папку
clear_folder(folder_to_clear)
