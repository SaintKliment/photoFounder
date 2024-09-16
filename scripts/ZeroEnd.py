def append_zero_to_lines(file_path):
    # Считываем строки из файла
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Добавляем " 0" в конце каждой строки
    updated_lines = [line.rstrip() + " 0\n" for line in lines]

    # Записываем обновленные строки обратно в файл
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

# Укажите путь к вашему файлу
file_path = './quaries/quaries.txt'
append_zero_to_lines(file_path)
