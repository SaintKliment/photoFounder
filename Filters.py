from PIL import Image
import cv2
import numpy as np
import requests
from io import BytesIO
import face_recognition
import os
import shutil

# проверка на разрешение
def is_high_resolution(image_path, min_resolution=(1024, 1024)):
    with Image.open(image_path) as img:
        return img.size[0] >= min_resolution[0] and img.size[1] >= min_resolution[1]

# проверка на качественный свет
def is_good_lighting(image_path, min_brightness_threshold=20, max_brightness_threshold=230, min_contrast_threshold=50, max_dark_pixels=0.1, max_bright_pixels=0.1): 
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Не удалось открыть изображение. Проверьте путь к файлу.")
    
    # Вычисление гистограммы и средней яркости
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256])
    mean_brightness = np.mean(histogram[0])
    
    # Вычисление контраста как разности между максимальным и минимальным значением яркости
    min_brightness = np.min(img)
    max_brightness = np.max(img)
    contrast = max_brightness - min_brightness
    
    # Проверка на яркость и контраст
    is_brightness_good = min_brightness_threshold < mean_brightness < max_brightness_threshold
    is_contrast_good = contrast > min_contrast_threshold
    
    # Проверка на процент темных и ярких пикселей
    dark_pixels_ratio = np.sum(img < min_brightness_threshold) / img.size
    bright_pixels_ratio = np.sum(img > max_brightness_threshold) / img.size
    
    is_dark_pixels_good = dark_pixels_ratio < max_dark_pixels
    is_bright_pixels_good = bright_pixels_ratio < max_bright_pixels
    
    return is_brightness_good and is_contrast_good and is_dark_pixels_good and is_bright_pixels_good

# фильтр на простой фон фото
def has_simple_background(image_path, threshold=0.5):
    # Загрузка модели DeepLabv3
    model = deeplabv3_resnet101(pretrained=True)
    model.eval()
    
    # Загрузка изображения и преобразование в формат для модели
    image = Image.open(image_path).convert('RGB')
    preprocess = T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    
    # Перенос данных на GPU если доступен, иначе на CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    input_batch = input_batch.to(device)
    
    # Выполнение сегментации
    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0).cpu().numpy()
    
    # Получаем маску фона (0 означает фон в DeepLabv3)
    background_mask = output_predictions == 0
    
    # Определяем процент фона
    background_ratio = background_mask.sum() / background_mask.size
    
    # Проверяем, является ли фон простым
    return background_ratio > threshold

# отбор по градусам поворота лица
def is_proper_angle(image_path, angle_threshold=10):
    image = face_recognition.load_image_file(image_path)
    face_landmarks_list = face_recognition.face_landmarks(image)
    
    if not face_landmarks_list:
        return False
    
    def angle_between_points(p1, p2):
        """Вычисляет угол между двумя точками"""
        delta_y = p2[1] - p1[1]
        delta_x = p2[0] - p1[0]
        return np.degrees(np.arctan2(delta_y, delta_x))
    
    def calculate_head_pose(landmarks):
        """Вычисляет угол наклона головы на основе лицевых точек"""
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']
        top_lip = landmarks['top_lip']
        bottom_lip = landmarks['bottom_lip']
        
        # Вычисление углов между точками глаз
        eye_angle = angle_between_points(left_eye[0], right_eye[3])
        
        # Вычисление угла между верхней и нижней губами
        mouth_angle = angle_between_points(top_lip[0], bottom_lip[3])
        
        return abs(eye_angle), abs(mouth_angle)
    
    angles = []
    for face_landmarks in face_landmarks_list:
        eye_angle, mouth_angle = calculate_head_pose(face_landmarks)
        angles.append((eye_angle, mouth_angle))
    
    # Проверка, что углы находятся в допустимом диапазоне для всех лиц
    for eye_angle, mouth_angle in angles:
        if eye_angle < angle_threshold and mouth_angle < angle_threshold:
            return True
    
    return False
    
# отбор по шуму
def is_low_noise(image_path, noise_threshold=10):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Не удалось открыть изображение. Проверьте путь к файлу.")
    
    # Применение медианного фильтра
    median = cv2.medianBlur(img, 3)
    
    # Вычисление шума как разности между оригинальным изображением и медианным фильтром
    noise = cv2.subtract(img, median)
    
    # Расчет среднеквадратичного отклонения шума
    noise_std = np.std(noise)
    
    # Проверка на низкий уровень шума
    return noise_std < noise_threshold

# отбор фото по эталону
#def has_consistent_style(image_path, reference_image_path):
#    img1 = cv2.imread(image_path)
#    img2 = cv2.imread(reference_image_path)
#    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
#    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
#    hist1 = cv2.normalize(hist1, hist1).flatten()
#    hist2 = cv2.normalize(hist2, hist2).flatten()
#    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL) > 0.9  # Примерный порог

def filter_images(directory, output_directory):
    # Создаем папку для отфильтрованных изображений, если она не существует
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Список поддерживаемых форматов изображений
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.heif', '.heic', '.raw')
    
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        
        # Проверяем, что это изображение в поддерживаемом формате
        if not filename.lower().endswith(supported_formats):
            continue
        
        if filename.lower().endswith('.webp'):
            print(f"{filename} is a WebP image and will be converted later.")
            continue
        
        if not is_high_resolution(image_path):
            continue
        if not is_good_lighting(image_path):
            continue
        if not has_simple_background(image_path):
            continue
        if not is_proper_angle(image_path):
            continue
        if not is_low_noise(image_path):
            continue
        # Если стиль важен, можно передать эталонное изображение
        # if not has_consistent_style(image_path, reference_image_path):
        #     continue
        
        # Перемещение отфильтрованного изображения в выходную папку
        shutil.copy(image_path, os.path.join(output_directory, filename))
        print(f"{filename} passed all checks and has been moved to {output_directory}.")

filter_images("./primary_photos", "./filters_photos")