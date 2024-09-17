import os
from deepface import DeepFace
import shutil

def analyze_gender(image_path):
    try:
        # Анализ пола с использованием DeepFace
        analysis = DeepFace.analyze(img_path=image_path, actions=['gender'], enforce_detection=False)
        
        # Проверка типа результата анализа
        if isinstance(analysis, list):
            analysis = analysis[0]
        
        # Проверка наличия нужного ключа в результате
        if 'gender' in analysis:
            return analysis['gender']
        else:
            print(f"Непредвиденный формат анализа для {image_path}: {analysis}")
            return 'Unknown'
    except Exception as e:
        print(f"Ошибка при анализе {image_path}: {e}")
        return 'Unknown'

def process_images(input_folder):
    results = []
    for img_name in os.listdir(input_folder):
        if img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
            img_path = os.path.join(input_folder, img_name)
            gender = analyze_gender(img_path)
            results.append((img_name, gender))
    
    return results

# Пример использования
output_folder = './workspace_photos/filters_photos'
input_folder = './workspace_photos/primary_photos'
results = process_images(input_folder)

# Вывод результатов
for img_name, gender_probs in results:
    woman_prob = gender_probs.get('Woman', 0)
    man_prob = gender_probs.get('Man', 0)
    if woman_prob > man_prob:
        src_path = os.path.join(input_folder, img_name)
        dest_path = os.path.join(output_folder, img_name)
        shutil.move(src_path, dest_path)  # Перемещение файла
        print(f"Изображение {img_name} перемещено в папку: {output_folder}")