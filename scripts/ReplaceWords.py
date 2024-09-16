def replace_word_in_file(file_path, old_word, new_word):
    # Открываем файл для чтения
    with open(file_path, 'r') as file:
        # Считываем содержимое файла
        content = file.read()

    # Заменяем старое слово на новое
    updated_content = content.replace(old_word, new_word)

    # Открываем файл для записи и записываем обновленное содержимое
    with open(file_path, 'w') as file:
        file.write(updated_content)

# Укажите путь к вашему файлу
file_path = './quaries/quaries.txt'
# Указываем старое и новое слово
old_word = '1'
new_word = ''

replace_word_in_file(file_path, old_word, new_word)