import cv2
import mediapipe as mp
import os

# Инициализация инструмента распознавания лица
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Путь к папке с изображениями
input_folder = './workspace_photos/primary_photos'
output_folder = './workspace_photos/filters_photos'

# Создание выходной папки, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Функция для вырезания лица и захвата волос
def crop_faces(image_path, output_path, margin=1):  # Увеличен margin для захвата волос
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Ошибка: не удалось загрузить изображение {image_path}")
        return
    
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        # Преобразование изображения в формат RGB для обработки
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_image)
        
        # Если лицо найдено
        if results.detections:
            for detection in results.detections:
                # Получение координат ограничивающей рамки
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                
                # Добавляем margin для захвата волос (расширяем область вырезания)
                margin_h = int(h * margin)
                margin_w = int(w * margin)
                
                x_new = max(0, x - margin_w)
                y_new = max(0, y - margin_h)
                w_new = min(iw - x_new, w + 2 * margin_w)
                h_new = min(ih - y_new, h + 2 * margin_h)
                
                # Вырезаем область лица с учетом волос
                cropped_face = image[y_new:y_new + h_new, x_new:x_new + w_new]

                if cropped_face.size == 0:
                    print(f"Ошибка: вырезанное изображение пустое для {image_path}")
                    return
                
                # Сохраняем вырезанное изображение головы
                cv2.imwrite(output_path, cropped_face)
                print(f"Сохранено: {output_path}")
        else:
            print(f"Лицо не найдено на {image_path}")

# Проход по папке с изображениями
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        crop_faces(image_path, output_path)
