import subprocess
import os

def run_python_scripts(scripts):
    for script in scripts:
        # Проверяем, существует ли скрипт
        if os.path.exists(script):
            print(f"Запуск скрипта: {script}")
            try:
                # Запускаем скрипт с помощью subprocess
                result = subprocess.run(['python', script], capture_output=True, text=True)
                
                # Проверяем результат
                if result.returncode == 0:
                    print(f"Скрипт {script} выполнен успешно.")
                else:
                    print(f"Ошибка при выполнении скрипта {script}. Код ошибки: {result.returncode}")
                    print(result.stderr)
            except Exception as e:
                print(f"Ошибка при запуске скрипта {script}: {e}")
        else:
            print(f"Скрипт {script} не найден.")

# Список скриптов для запуска
scripts_to_run = [
    './scripts/DelDubl.py',
    './scripts/Cut_faces.py',
    #'./scripts/DelBadColor.py',
    './scripts/Numeration.py'
]

# Запуск скриптов
run_python_scripts(scripts_to_run)
