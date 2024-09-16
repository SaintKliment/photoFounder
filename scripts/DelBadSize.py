import os

# Путь к папке с изображениями
folder_path = './workspace_photos/primary_photos'

# Минимальный размер файла в байтах (350 КБ = 350 * 1024 байт)
min_file_size = 350 * 1024  # 350 КБ

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Проверяем, является ли файл изображением
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif')):
        print(f"Пропущен не изображение: {filename}")
        continue
    
    # Получаем размер файла в байтах
    file_size = os.path.getsize(file_path)
    
    # Если размер файла меньше минимального значения, удаляем его
    if file_size < min_file_size:
        os.remove(file_path)
        print(f"Удалено: {filename} (Размер: {file_size / 1024:.2f} КБ)")
