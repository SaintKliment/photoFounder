import cv2
import os
import numpy as np

# Папка с изображениями
input_folder = '../filters_photos'

# Удаление изображений с низкой насыщенностью (серые) или мультяшным цветокором
def remove_unwanted_images(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        return False
    
    # Преобразуем изображение в HSV (Hue, Saturation, Value) формат
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Получаем среднюю насыщенность изображения
    saturation = hsv_image[:, :, 1]
    mean_saturation = np.mean(saturation)

    # Порог для удаления серых изображений (например, если средняя насыщенность ниже 50)
    if mean_saturation < 50:
        print(f"Удаление серого изображения: {image_path}")
        os.remove(image_path)
        return True

    # Для мультяшных изображений можно проверить контраст по каждому каналу
    mean_stddev = np.std(image, axis=(0, 1))  # Стандартное отклонение по каждому каналу
    
    # Порог для мультяшного цветокора (если стандартное отклонение слишком велико)
    if np.any(mean_stddev > 70):  # Например, если контраст больше 70 для любого канала
        print(f"Удаление изображения с мультяшным цветокором: {image_path}")
        os.remove(image_path)
        return True

    return False

# Проход по всем изображениям в папке
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        image_path = os.path.join(input_folder, filename)
        remove_unwanted_images(image_path)
