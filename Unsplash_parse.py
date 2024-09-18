import os
import requests

ACCESS_KEY = 'T-f6wQSdHcXSkGRpT6ochprrKMBwkN0E9Oi18bkcqBc'

def fetch_unsplash_related_photos(photo_id):
    url = f'https://api.unsplash.com/photos/{photo_id}/related'
    
    params = {
        'client_id': ACCESS_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # print(data)  # Выводим данные для отладки
        return data['results']  # Возвращаем только результаты
    else:
        print(f"Error fetching: {response.status_code}")
        return []

def download_photo(photo_url, folder_path, photo_index):
    try:
        response = requests.get(photo_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Define the file name and path with the provided index
        file_name = f"photo_{photo_index}.jpg"  # Изменено на photo_index
        file_path = os.path.join(folder_path, file_name)

        # Write the photo to a file
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download {photo_url}: {e}")

def main(photo_id, folder_path, start_index=1):  # Добавлено начальное значение
    photos = fetch_unsplash_related_photos(photo_id)

    if isinstance(photos, list):  # Проверяем, что это список
        for index, photo in enumerate(photos):
            if isinstance(photo, dict) and 'urls' in photo:  # Проверяем формат данных
                photo_url = photo['urls']['regular']  # Получаем URL изображения
                download_photo(photo_url, folder_path, start_index + index)  # Используем start_index
            else:
                print(f"Unexpected data format for photo: {photo}")
    else:
        print("No photos found or invalid data format.")

if __name__ == "__main__":
    main(photo_id='BGMuQUY91w4', folder_path='./workspace_photos/primary_photos', start_index=1)  # Устанавливаем начальный индекс
