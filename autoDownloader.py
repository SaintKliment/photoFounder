import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
from urllib.parse import quote
import re

# Путь к веб-драйверу
driver_path = r'C:\Users\kali\Documents\PhotoFounder\PhotoFounder\driver\chromedriver.exe'

# Настройка опций для Chrome
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.121 Safari/537.36")
chrome_options.add_argument('--ssl-protocol=any')
chrome_options.add_argument('--disable-ssl-encryption')
chrome_options.add_argument('--no-sandbox')

# Создаем сервис для ChromeDriver
service = Service(executable_path=driver_path)

# Инициализация веб-драйвера с использованием сервиса и опций
driver = webdriver.Chrome(service=service, options=chrome_options)

prev_img_url = None  # Инициализируем переменную для хранения предыдущего img_url

def view_images(query, save_folder, counter, additional_pass, photos_to_download):
    global prev_img_url  # Используем глобальную переменную для сохранения предыдущего URL
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    search_url = f"https://yandex.ru/images/search?text={query}&size=large&icolor=color"
    driver.get(search_url)
    if counter == 0:
        input("Пройдите капчу и нажмите Enter для продолжения...\n")
    time.sleep(3)
    
    first_image_link = driver.find_element(By.XPATH, '//a[contains(@class,"Link ContentImage-Cover")]')
    first_image_href = first_image_link.get_attribute('href')
    driver.execute_script(f"window.open('{first_image_href}', '_blank');")
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])

    downloaded = 0  # Счетчик загруженных изображений

    while downloaded < photos_to_download:
        if counter == 0:
            while additional_pass > 0:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)
                additional_pass -= 1
                time.sleep(1.5)

        if additional_pass == 0:
            time.sleep(3)
            additional_pass -= 1

        try:
            # Нажимаем кнопку для выбора размера изображения
            sizes_button = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.OpenImageButton-SizesButton'))
            )
            sizes_button.click()  # Кликаем на кнопку, чтобы открыть размеры
            
            # Ждем, пока элемент с ссылкой на изображение станет доступным
            image_link_element = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.OpenImageButton-ListItem'))
            )
            image_url = image_link_element.get_attribute("href")
           
            # Получаем данные изображения для проверки размера
            img_data = requests.get(image_url).content
            img = Image.open(BytesIO(img_data))
            width, height = img.size

            # Проверяем размеры изображения
            if width >= 1000 and height >= 1000:
                # Скачиваем изображение
                print(f"Скачиваем изображение: {image_url}")

                img_format = image_url.split('.')[-1].split('?')[0]
                img_name = f"image_{counter + 1}.{img_format}"
                img_path = os.path.join(save_folder, img_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)

                print(f"Сохранено: {img_name}")
                counter += 1
                downloaded += 1  # Увеличиваем количество загруженных изображений
            else:
                print(f"Пропущено (размер меньше 1000x1000): {image_url}")

            time.sleep(3)

        except Exception as e:
                print(f"Ошибка при поиске или скачивании изображения: {e}")


        
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)
        time.sleep(3)

    return counter

def close_all_but_first_tab():
    # Получаем список всех открытых вкладок
    all_tabs = driver.window_handles
    # Переключаемся на первую вкладку
    driver.switch_to.window(all_tabs[0])
    # Закрываем все вкладки, кроме первой
    for tab in all_tabs[1:]:
        driver.switch_to.window(tab)
        driver.close()
    # Возвращаемся к первой вкладке
    driver.switch_to.window(all_tabs[0])

def process_file(file_path, save_folder, photos_to_download):
    counter = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        query = re.sub(r'\s+0$', '', line.strip())  # Убираем число 0 и пробелы перед ним
        query = quote(query)
        status = line.strip()[-1]  # Получаем последний символ, который является 0 или 1

        if status == '0':  # Если строка не обработана
            counter = view_images(query, save_folder, counter, 0, photos_to_download)

            # Обновляем статус строки
            lines[index] = f"{query} 1\n"
            
            # Сохраняем изменения в файл после завершения запроса
            with open(file_path, 'w') as file:
                file.writelines(lines)
            print(f"Обработано {photos_to_download} изображений. Обновляем запрос: {query}")
            
            # Закрываем все вкладки, кроме первой
            close_all_but_first_tab()

# Запуск процесса
file_path = './quaries/quaries6.txt'
save_folder = './workspace_photos/primary_photos'
photos_to_download = 250  # Указываем количество фотографий для скачивания на один запрос
process_file(file_path, save_folder, photos_to_download)