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
from selenium.webdriver.common.action_chains import ActionChains


# Путь к веб-драйверу
driver_path = r'C:\Users\kali\Documents\PhotoFounder\PhotoFounder\driver\chromedriver.exe'

# Настройка опций для Chrome
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.121 Safari/537.36")
chrome_options.add_argument('--ignore-certificate-errors')  # Игнорирование ошибок сертификатов
chrome_options.add_argument('--disable-web-security')  # Отключение безопасности веб-страниц
chrome_options.add_argument('--allow-running-insecure-content')  # Разрешение небезопасного контента
chrome_options.add_argument('--disable-gpu')  # Отключение GPU (иногда помогает с ошибками)
chrome_options.add_argument('--user-data-dir=/path/to/your/custom/profile')

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

def search_query(query):
    # Ввод текста в поле поиска
    try:
        # Ожидание появления поля поиска
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-id="search-box-input"]'))
        )

        # Ввод текста в поле поиска
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        print(f"Поиск выполнен для запроса: {query}")
    except Exception as e:
        print(f"Ошибка при вводе текста в поле поиска: {e}")

    # Подождем, пока результаты поиска загрузятся
    time.sleep(5)

# Инициализируем счетчик вне функции
counter = 1

# Функция для скачивания изображений
def download_image(img_url, save_path, spec_modified_img):
    global counter  # будем использовать глобальную переменную counter
    try:
        # Определяем имя файла
        img_name = f"img_{counter}.jpg"
        img_path = os.path.join(save_path, img_name)
        
        # Скачиваем изображение
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            if width >= 1024 and height >= 1024:  # укажите минимально допустимые размеры
                addToDownloads(spec_modified_img)
                with open(img_path, 'wb') as file:
                    file.write(response.content)
                print(f"Изображение сохранено как {img_path}")
                counter += 1
            else:
                print(f"Изображение {img_url} пропущено, так как его размер не подходит.")
        else:
            print(f"Не удалось скачать изображение. Статус код: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения: {e}")

# Пролистывание страницы и скачивание изображений
# Пролистывание страницы и скачивание изображений с плавным скроллингом
def smooth_scroll_and_download_images(scroll_pause_time=2, scroll_step=300):
    last_height = driver.execute_script("return document.body.scrollHeight")

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
                img_src = img_element.get_attribute('src')
                
                # Модифицируем img_src для получения оригинального изображения
                img_src_parts = img_src.split('/')
                modified_img_src = f"https://i.pinimg.com/originals/{'/'.join(img_src_parts[4:7])}/{img_src_parts[-1]}"
                modified_img_src_parts = modified_img_src.split('/')
                spec_modified_img = '/'.join(modified_img_src_parts[4:])

                if isUniquePhoto(spec_modified_img) == True:
                    download_image(modified_img_src, save_path, spec_modified_img)
                else:
                    print("Duplicate image detected, skipping.")
                time.sleep(5)
            except Exception as e:
                print(f"Ошибка при скачивании изображения: {e}")
        
        # Прокрутка страницы вниз небольшими шагами
        for i in range(0, last_height, scroll_step):
            driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(0.1)  # Пауза для плавности скролла

        # Ждем, пока страница подгрузит новые изображения
        time.sleep(scroll_pause_time)
        
        # Проверка изменения высоты страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Достигнут конец страницы, больше изображений не подгружается.")
            break
        last_height = new_height

downloads_links = []
def addToDownloads(modified_img_src):
    global downloads_links
    downloads_links.append(modified_img_src)
    if len(downloads_links) > 50:
        # Удаляем первые 10 элементов
        del downloads_links[:10]

def isUniquePhoto(spec_modified_img):
    for i in downloads_links:
        if i == spec_modified_img:
            return False
    return True

search_query("pretty face")

# Создание папки для сохранения фотографий
save_path = './workspace_photos/primary_photos'
os.makedirs(save_path, exist_ok=True)

# Запуск функции для пролистывания страницы и скачивания изображений
smooth_scroll_and_download_images()

# Пауза, чтобы увидеть результат (опционально)
input("Нажмите Enter для закрытия браузера...")

# Закрытие браузера
driver.quit()
