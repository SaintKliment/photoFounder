import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Путь к веб-драйверу
driver_path = r'C:\Users\kali\Documents\PhotoFounder\PhotoFounder\driver\chromedriver.exe'

# Настройка опций для Chrome
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Создаем сервис для ChromeDriver
service = Service(executable_path=driver_path)

# Инициализация веб-драйвера с использованием сервиса и опций
driver = webdriver.Chrome(service=service, options=chrome_options)

def view_images(query, save_folder, counter):
    # Создаем папку для сохранения изображений, если она не существует
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Формируем URL запроса
    search_url = f"https://yandex.ru/images/search?text={query}"

    # Открываем страницу
    driver.get(search_url)

    # Пауза для прохождения капчи
    input("Пройдите капчу и нажмите Enter для продолжения...")

    # Подождите немного, чтобы убедиться, что страница полностью загружена после прохождения капчи
    time.sleep(3)

    # Ищем первый элемент, который может быть изображением
    first_image_link = driver.find_element(By.XPATH, '//a[contains(@class,"Link ContentImage-Cover")]')
    first_image_href = first_image_link.get_attribute('href')
    
    # Открываем первое изображение в новой вкладке
    driver.execute_script(f"window.open('{first_image_href}', '_blank');")
    time.sleep(3)  # Даем время на открытие новой вкладки

    # Переключаемся на новую вкладку
    driver.switch_to.window(driver.window_handles[-1])
    
    # Листаем изображения
    while True:
        # Пауза, чтобы увидеть текущее изображение
        time.sleep(3)
        
        try:
            print("Ищем блок с изображением...")
            
            # Пробуем найти блок с классами SwipeImage и MMImageWrapper
            image_wrapper = driver.find_element(By.CSS_SELECTOR, 'div.SwipeImage.MMImageWrapper')
            print("Блок с изображением найден.")

            # Используем ActionChains для имитации правого клика по изображению
            action = ActionChains(driver)
            action.context_click(image_wrapper).perform()  # Правый клик
           
            

            # Найти полноразмерное изображение внутри блока
            full_size_img = image_wrapper.find_element(By.CSS_SELECTOR, 'img.MMImage-Origin')
            img_url = full_size_img.get_attribute('src')


            if img_url.startswith('//'):
                img_url = 'https:' + img_url

            print(f"Скачиваем изображение {counter + 1}: {img_url}")
            
            # Скачиваем изображение
            img_data = requests.get(img_url).content
            # Определяем формат изображения
            img_format = img_url.split('.')[-1].split('?')[0]  # Убираем параметры после "?"
            if img_format.lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'webp', 'heif', 'heic', 'raw']:
                # Сохраняем изображение
                img_name = f"image_{counter + 1}.{img_format}"
                img_path = os.path.join(save_folder, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Сохранено: {img_name}")
                counter += 1
            else:
                print(f"Пропущено (неизвестный формат): {img_url}")

            # Пауза после скачивания изображения
            time.sleep(6)  # Даем время, чтобы не перегружать сервер

        except Exception as e:
            print(f"Ошибка при поиске полноразмерного изображения: {e}")
        
        # Листаем на следующее изображение
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)
        # Пауза между прокрутками изображений
        time.sleep(6)  # Увеличено время ожидания между прокрутками

# Пример использования
view_images('female pretty face', save_folder='primary_photos', counter=0)  # ваш запрос
