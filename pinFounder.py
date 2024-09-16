from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
import os
from PIL import Image
from io import BytesIO

# Путь к вашему веб-драйверу
driver_path = r'C:\Users\kali\Documents\PhotoFounder\PhotoFounder\driver\chromedriver.exe'

# Настройка опций для Chrome
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.121 Safari/537.36")
chrome_options.add_argument('--ignore-certificate-errors')  # Игнорирование ошибок сертификатов
chrome_options.add_argument('--disable-web-security')  # Отключение безопасности веб-страниц
chrome_options.add_argument('--allow-running-insecure-content')  # Разрешение небезопасного контента
chrome_options.add_argument('--disable-gpu')  # Отключение GPU (иногда помогает с ошибками)

# Создаем сервис для ChromeDriver
service = Service(executable_path=driver_path)

# Инициализация веб-драйвера с использованием сервиса и опций
driver = webdriver.Chrome(service=service, options=chrome_options)

# Открытие сайта Pinterest
driver.get('https://www.pinterest.com/')

# Подождем, пока кнопка "Просмотреть" станет доступной, и нажмем на нее
try:
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/ideas/")]')))
    button.click()
    print("Кнопка 'Просмотреть' нажата успешно.")
except Exception as e:
    print(f"Ошибка при нажатии на кнопку: {e}")

# Подождем немного, чтобы страница обновилась
time.sleep(5)

# Ввод текста в поле поиска
try:
    # Ожидание появления поля поиска
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-id="search-box-input"]'))
    )
    
    # Ввод текста в поле поиска
    query = "high resolution female face"  # Здесь нужно подставить ваш запрос
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    print(f"Поиск выполнен для запроса: {query}")
except Exception as e:
    print(f"Ошибка при вводе текста в поле поиска: {e}")

# Подождем, пока результаты поиска загрузятся
time.sleep(5)

# Создание папки для сохранения фотографий
save_path = './workspace_photos/primary_photos'
os.makedirs(save_path, exist_ok=True)

# Счётчик для имени файлов
counter = 1

# Функция для скачивания изображений
def download_image(img_url, save_path, index):
    try:
        # Определяем имя файла
        img_name = f"img_{index}.jpg"
        img_path = os.path.join(save_path, img_name)
        
        # Скачиваем изображение
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            if width > 150 and height > 150: #  укажите минимально допустимые размеры
                with open(img_path, 'wb') as file:
                    file.write(response.content)
                print(f"Изображение сохранено как {img_path}")
            else:
                print(f"Изображение {img_url} пропущено, так как его размер меньше нужных пикселей.")
        else:
            print(f"Не удалось скачать изображение. Статус код: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения: {e}")

# Пролистывание страницы и скачивание изображений
def scroll_and_download_images():
    global counter
    while True:
        # Найти все изображения на странице
        img_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "XiG") and contains(@class, "zI7") and contains(@class, "iyn") and contains(@class, "Hsu")]/img')
        if not img_elements:
            print("Изображения не найдены.")
            break
        
        # Скачать каждое изображение
        for img_element in img_elements:
            try:
                # Получаем URL изображения
                img_url = img_element.get_attribute('src')
                if img_url:
                    download_image(img_url, save_path, counter)
                    counter += 1
            except Exception as e:
                print(f"Ошибка при скачивании изображения: {e}")
        
        # Прокрутка страницы вниз для загрузки новых изображений
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Подождем, пока загрузятся новые изображения

# Запуск функции для пролистывания страницы и скачивания изображений
scroll_and_download_images()

# Пауза, чтобы увидеть результат (опционально)
input("Нажмите Enter для закрытия браузера...")

# Закрытие браузера
driver.quit()
