import cv2
import numpy as np
import os

# Загружаем предобученные каскады Хаара для анфас и профильного лица
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

# Путь к папке, где будут сохраняться маски
output_folder = './workspace_photos/binary_masks'
os.makedirs(output_folder, exist_ok=True)

# Функция для увеличения охвата прямоугольника
def expand_rect(x, y, w, h, scale=2.0):
    # Рассчитываем новый размер и смещение, чтобы центр оставался прежним
    new_w = int(w * scale)
    new_h = int(h * scale)
    new_x = int(x - (new_w - w) / 2)
    new_y = int(y - (new_h - h) / 2)
    return new_x, new_y, new_w, new_h

# Функция для детекции лиц и создания бинарной маски
def detect_faces_and_create_mask(image_path, scale=2.0):
    # Загружаем изображение
    img = cv2.imread(image_path)
    if img is None:
        print(f"Ошибка загрузки изображения {image_path}")
        return
    
    # Преобразуем изображение в градации серого для работы каскадов Хаара
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Детекция анфас
    faces_frontal = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Детекция профиля
    faces_profile = profile_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Создаем пустую маску того же размера, что и изображение
    mask = np.zeros_like(gray)
    
    # Заполняем маску белым в местах, где найдены лица (анфас), с увеличенным охватом
    for (x, y, w, h) in faces_frontal:
        x_exp, y_exp, w_exp, h_exp = expand_rect(x, y, w, h, scale)
        # Убеждаемся, что координаты внутри изображения
        x_exp = max(0, x_exp)
        y_exp = max(0, y_exp)
        w_exp = min(w_exp, mask.shape[1] - x_exp)
        h_exp = min(h_exp, mask.shape[0] - y_exp)
        mask[y_exp:y_exp+h_exp, x_exp:x_exp+w_exp] = 255
    
    # Заполняем маску белым в местах, где найдены лица (профиль), с увеличенным охватом
    for (x, y, w, h) in faces_profile:
        x_exp, y_exp, w_exp, h_exp = expand_rect(x, y, w, h, scale)
        x_exp = max(0, x_exp)
        y_exp = max(0, y_exp)
        w_exp = min(w_exp, mask.shape[1] - x_exp)
        h_exp = min(h_exp, mask.shape[0] - y_exp)
        mask[y_exp:y_exp+h_exp, x_exp:x_exp+w_exp] = 255
    
    # Сохраняем бинарную маску в папку output_folder
    base_filename = os.path.basename(image_path)
    mask_filename = os.path.join(output_folder, f"mask_{base_filename}")
    cv2.imwrite(mask_filename, mask)
    print(f"Маска сохранена: {mask_filename}")

# Пример использования
image_path = './workspace_photos/primary_photos/img_8.jpg'  # путь к вашему изображению
detect_faces_and_create_mask(image_path, scale=2.0)
