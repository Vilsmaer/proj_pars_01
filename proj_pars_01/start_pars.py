# start_pars.py — Полный автоматизированный запуск парсинга и анализа

import os
import subprocess
import sys

# === КОНФИГУРАЦИЯ: УКАЗЫВАЕМ ПОЛНЫЕ ПУТИ ===
BASE_DIR = r"D:\ANKO\proj_pars_01"

# Пути к входным/выходным файлам
SITEMAP_FILE = os.path.join(BASE_DIR, "Pasted_Text.txt")
FILTERED_URLS_FILE = os.path.join(BASE_DIR, "filtered_product_urls.txt")
ALL_PRODUCTS_CSV = os.path.join(BASE_DIR, "all_products.csv")
PRODUCTS_XLSX = os.path.join(BASE_DIR, "products.xlsx")
ANALYSIS_REPORT = os.path.join(BASE_DIR, "analysis_report.xlsx")

# Пути к скриптам (полные!)
SCRIPT_FILTR = os.path.join(BASE_DIR, "filtr.py")
SCRIPT_PARSE = os.path.join(BASE_DIR, "parse_all_products.py")
SCRIPT_FORMAT = os.path.join(BASE_DIR, "format_to_excel.py")
SCRIPT_ANALYZE = os.path.join(BASE_DIR, "analyze_products.py")

# Проверяем, что все скрипты существуют
for script_path in [SCRIPT_FILTR, SCRIPT_PARSE, SCRIPT_FORMAT, SCRIPT_ANALYZE]:
    if not os.path.exists(script_path):
        print(f" ОШИБКА: Скрипт не найден: {script_path}")
        sys.exit(1)

# Проверяем, что sitemap существует
if not os.path.exists(SITEMAP_FILE):
    print(f" ОШИБКА: Файл sitemap не найден: {SITEMAP_FILE}")
    sys.exit(1)


# === ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ: Запуск скрипта с логированием ===
def run_script(script_name, script_path):
    print(f"\n ЗАПУСК: {script_name} ({script_path})")
    print("-" * 60)

    try:
        # Запускаем скрипт через тот же интерпретатор Python
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=BASE_DIR  # Рабочая директория — папка проекта
        )

        if result.returncode == 0:
            print(f" {script_name}: УСПЕШНО ЗАВЕРШЁН")
            if result.stdout.strip():
                print(" Вывод скрипта:")
                print(result.stdout)
        else:
            print(f" {script_name}: ОШИБКА (код {result.returncode})")
            if result.stderr.strip():
                print("❗ Ошибки:")
                print(result.stderr)
            sys.exit(1)

    except Exception as e:
        print(f" КРИТИЧЕСКАЯ ОШИБКА при запуске {script_name}: {e}")
        sys.exit(1)


# === ОСНОВНОЙ ПРОЦЕСС ===
if __name__ == "__main__":
    print(" СТАРТ АВТОМАТИЧЕСКОГО ПАРСИНГА И АНАЛИЗА")
    print("=" * 60)

    # ШАГ 1: Фильтрация URL
    run_script("Фильтрация URL из sitemap", SCRIPT_FILTR)

    # Проверяем, что файл с URL создан
    if not os.path.exists(FILTERED_URLS_FILE):
        print(f" Файл с URL не создан: {FILTERED_URLS_FILE}")
        sys.exit(1)
    else:
        with open(FILTERED_URLS_FILE, "r", encoding="utf-8") as f:
            url_count = len([line for line in f if line.strip()])
        print(f" Найдено {url_count} URL товаров")

    # ШАГ 2: Парсинг всех товаров
    run_script("Парсинг всех товаров", SCRIPT_PARSE)

    # Проверяем, что CSV создан
    if not os.path.exists(ALL_PRODUCTS_CSV):
        print(f" Файл all_products.csv не создан")
        sys.exit(1)
    else:
        print(f" Файл all_products.csv успешно создан")

    # ШАГ 3: Преобразование в Excel
    run_script("Преобразование в Excel", SCRIPT_FORMAT)

    # Проверяем, что Excel создан
    if not os.path.exists(PRODUCTS_XLSX):
        print(f" Файл products.xlsx не создан")
        sys.exit(1)
    else:
        print(f" Файл products.xlsx успешно создан")

    # ШАГ 4: Анализ данных
    run_script("Анализ данных", SCRIPT_ANALYZE)

    # Проверяем, что отчёт создан
    if not os.path.exists(ANALYSIS_REPORT):
        print(f" Файл analysis_report.xlsx не создан")
        sys.exit(1)
    else:
        print(f" Файл analysis_report.xlsx успешно создан")

    # === ГОТОВО ===
    print("\n" + "=" * 60)
    print(" ВСЕ ЭТАПЫ УСПЕШНО ЗАВЕРШЕНЫ!")
    print(" Результаты:")
    print(f"  - Таблица товаров: {PRODUCTS_XLSX}")
    print(f"  - Аналитический отчёт: {ANALYSIS_REPORT}")
    print("=" * 60)