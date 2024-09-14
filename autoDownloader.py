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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.121 Safari/537.36")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--allow-running-insecure-content')

# Создаем сервис для ChromeDriver
service = Service(executable_path=driver_path)

# Инициализация веб-драйвера с использованием сервиса и опций
driver = webdriver.Chrome(service=service, options=chrome_options)

def view_images(query, save_folder, counter, additional_pass, photos_to_download):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    search_url = f"https://yandex.ru/images/search?text={query}"
    driver.get(search_url)
    if counter == 0:
        input("Пройдите капчу и нажмите Enter для продолжения...")
    time.sleep(3)

    first_image_link = driver.find_element(By.XPATH, '//a[contains(@class,"Link ContentImage-Cover")]')
    first_image_href = first_image_link.get_attribute('href')
    driver.execute_script(f"window.open('{first_image_href}', '_blank');")
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])

    downloaded = 0  # Счетчик загруженных изображений
    
    while downloaded < photos_to_download:
        while additional_pass > 0:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RIGHT)
            additional_pass -= 1
            time.sleep(1.5)
        
        if additional_pass == 0:
            time.sleep(3)
            additional_pass -= 1

        try:
            print("Ищем блок с изображением...")
            image_wrapper = driver.find_element(By.CSS_SELECTOR, 'div.SwipeImage.MMImageWrapper')
            print("Блок с изображением найден.")
            action = ActionChains(driver)
            action.context_click(image_wrapper).perform()
            full_size_img = image_wrapper.find_element(By.CSS_SELECTOR, 'img.MMImage-Origin')
            img_url = full_size_img.get_attribute('src')  # Используем get_attribute вместо getAttribute

            if img_url.startswith('//'):
                img_url = 'https:' + img_url

            print(f"Скачиваем изображение {counter + 1}: {img_url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.121 Safari/537.36',
                'Referer': driver.current_url
                }
            img_data = requests.get(img_url, headers=headers, timeout=10).content
            img_format = img_url.split('.')[-1].split('?')[0]

            if img_format.lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'webp', 'heif', 'heic', 'raw']:
                img_name = f"image_{counter + 1}.{img_format}"
                img_path = os.path.join(save_folder, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Сохранено: {img_name}")
                counter += 1
                downloaded += 1  # Увеличиваем количество загруженных изображений
            else:
                print(f"Пропущено (неизвестный формат): {img_url}")
            time.sleep(3)

        except Exception as e:
            print(f"Ошибка при поиске полноразмерного изображения: {e}")
        
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
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        query = line.strip()[:-2].strip()  # Получаем запрос без пробела и статуса
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
file_path = './quaries/quaries5.txt'
save_folder = 'primary_photos'
photos_to_download = 250  # Указываем количество фотографий для скачивания на один запрос
process_file(file_path, save_folder, photos_to_download)