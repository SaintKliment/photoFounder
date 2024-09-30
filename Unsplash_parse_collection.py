import requests
import os

# Ваш API-ключ
ACCESS_KEY = 'T-f6wQSdHcXSkGRpT6ochprrKMBwkN0E9Oi18bkcqBc'

# ID коллекции
COLLECTION_ID = 'Ych4dudwato'

# Папка для сохранения
SAVE_DIR = './workspace_photos/primary_photo'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_photos_from_collection(collection_id, page=1, per_page=30):
    url = f'https://api.unsplash.com/collections/{collection_id}/photos'
    headers = {'Authorization': f'Client-ID {ACCESS_KEY}'}
    params = {'page': page, 'per_page': per_page}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Ошибка: {response.status_code}')
        return []

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Скачано: {filename}')
    else:
        print(f'Не удалось скачать изображение: {url}')

# Получаем фото и сохраняем
photos = get_photos_from_collection(COLLECTION_ID)

for photo in photos:
    image_url = photo['urls']['full']  # Максимальное разрешение
    image_id = photo['id']
    filename = os.path.join(SAVE_DIR, f'{image_id}.jpg')

    download_image(image_url, filename)