import os
import subprocess
import time

# Путь к файлу со строками
values_file = './queries/queries3.txt'
# Путь к папке для сохранения изображений
save_folder = 'primary_photos'
# Путь к скрипту для запуска
script_to_run = 'yandex_photo_founder.py'
# Количество фото для скачивания перед перезапуском
batch_size = 750

def get_queries_from_file(file_path):
    queries = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                query, status = parts
                if status == '0':
                    queries.append(query)
    return queries

def write_queries_to_file(file_path, queries):
    with open(file_path, 'w') as file:
        for query in queries:
            file.write(f"{query}\t1\n")  # Обновляем статус на 1

def update_query_status(file_path, query):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith(query):
                file.write(f"{query}\t1\n")
            else:
                file.write(line)

def run_script_with_params(script_path, query, counter):
    command = ['python', script_path, query, save_folder, str(counter)]
    subprocess.run(command, check=True)

def main():
    queries = get_queries_from_file(values_file)
    query_index = 0
    counter = 0
    
    while query_index < len(queries):
        query = queries[query_index]
        print(f"Запускаем скрипт для запроса: {query} с counter={counter}")
        
        # Запускаем основной скрипт
        run_script_with_params(script_to_run, query, counter)
        
        # Обновляем статус запроса в файле
        update_query_status(values_file, query)
        
        # Обновляем счётчик
        counter += batch_size
        
        # Проверка, если мы достигли конца списка запросов, выход из цикла
        if query_index + 1 >= len(queries):
            break
        
        # Переход к следующему запросу
        query_index += 1

        # Пауза перед запуском следующего запроса
        time.sleep(10)

if __name__ == "__main__":
    main()
