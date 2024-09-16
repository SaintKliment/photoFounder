import cv2
import os
import numpy as np

# Папка для сохранения итоговых изображений
masked_images_folder = './workspace_photos/masked_images'
os.makedirs(masked_images_folder, exist_ok=True)

# Функция для применения маски и сохранения результата
def apply_mask(image_path, mask_path):
    # Загружаем исходное изображение
    img = cv2.imread(image_path)
    if img is None:
        print(f"Ошибка загрузки изображения {image_path}")
        return
    
    # Загружаем маску
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Ошибка загрузки маски {mask_path}")
        return
    
    # Проверяем, что размеры изображения и маски совпадают
    if img.shape[:2] != mask.shape[:2]:
        print("Размеры изображения и маски не совпадают!")
        return
    
    # Преобразуем маску в трёхканальный формат, чтобы использовать ее для цветного изображения
    mask_3channel = cv2.merge([mask, mask, mask])
    
    # Применяем маску к изображению (используем побитовую операцию AND)
    masked_img = cv2.bitwise_and(img, mask_3channel)
    
    # Сохраняем итоговое изображение в папку masked_images
    base_filename = os.path.basename(image_path)
    masked_filename = os.path.join(masked_images_folder, f"masked_{base_filename}")
    cv2.imwrite(masked_filename, masked_img)
    print(f"Результат сохранен: {masked_filename}")

# Пример использования
image_path = './workspace_photos/primary_photos/img_8.jpg' # путь к вашему изображению
mask_path = './workspace_photos/binary_masks/mask_img_8.jpg'  # путь к соответствующей маске
apply_mask(image_path, mask_path)
