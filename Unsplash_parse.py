import os
import requests

ACCESS_KEY = 'T-f6wQSdHcXSkGRpT6ochprrKMBwkN0E9Oi18bkcqBc'

# Функция для получения связанных фотографий с Unsplash API
def fetch_unsplash_related_photos(photo_id):
    url = f'https://api.unsplash.com/photos/{photo_id}/related'
    
    params = {
        'client_id': ACCESS_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['results']  # Возвращаем только результаты
    else:
        print(f"Error fetching: {response.status_code}")
        return []

# Функция для загрузки фотографии по URL
def download_photo(photo_url, folder_path, photo_index):
    try:
        response = requests.get(photo_url)
        response.raise_for_status()  # Вызывает ошибку для некорректных ответов

        # Создаем папку, если она не существует
        os.makedirs(folder_path, exist_ok=True)

        # Определяем имя и путь к файлу с использованием индекса
        file_name = f"photo_{photo_index}.jpg"
        file_path = os.path.join(folder_path, file_name)

        # Записываем фото в файл
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download {photo_url}: {e}")

# Основная функция
def main(photo_id, folder_path, start_index=1):
    photos = fetch_unsplash_related_photos(photo_id)

    if isinstance(photos, list):  # Проверяем, что получены данные в формате списка
        for index, photo in enumerate(photos):
            if isinstance(photo, dict) and 'urls' in photo:  # Проверяем формат данных
                # Используем 'raw' или 'full' для наивысшего качества
                photo_url = photo['urls'].get('raw', photo['urls']['full'])
                download_photo(photo_url, folder_path, start_index + index)  # Используем start_index
            else:
                print(f"Unexpected data format for photo: {photo}")
    else:
        print("No photos found or invalid data format.")

if __name__ == "__main__":
    main(photo_id='U4JDjYmjn1g', folder_path='./workspace_photos/primary_photos', start_index=121)  # Устанавливаем начальный индекс
