# parse_all_products.py — Парсим все товары из списка URL

import requests
from bs4 import BeautifulSoup
import csv
import re
import time

# === КОНФИГУРАЦИЯ ===
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}
# УКАЗЫВАЕМ ПРЯМОЙ ПУТЬ К ФАЙЛУ
INPUT_FILE = r"D:\ANKO\proj_pars_01\filtered_product_urls.txt"
#OUTPUT_FILE = "all_products.csv"  # можно тоже сделать полным, если нужно
OUTPUT_FILE = r"D:\ANKO\proj_pars_01\all_products.csv"


# === ФУНКЦИЯ: Извлечь цену из текста ===
def extract_price(price_text: str) -> float:
    if not price_text:
        return 0.0
    clean = re.sub(r'[^\d]', '', price_text)  # оставляем только цифры
    try:
        return float(clean) if clean else 0.0
    except ValueError:
        return 0.0


# === ФУНКЦИЯ: Парсинг одной страницы товара ===
def parse_product_page(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    data = {"url": url}

    # 🔹 НАЗВАНИЕ — из <h1>
    title_tag = soup.select_one('h1')
    data["name"] = title_tag.get_text(strip=True) if title_tag else "Без названия"

    # 🔹 ЦЕНА — ищем по классу .price_value
    price_tag = soup.select_one('.price_value')
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    data["price"] = extract_price(price_text)
    data["price_raw"] = price_text

    # 🔹 НАЛИЧИЕ — ищем текст "В наличии: X"
    availability_tag = soup.find(string=re.compile(r'В наличии'))
    if availability_tag:
        match = re.search(r'В наличии:\s*(\d+)', availability_tag)
        data["in_stock"] = int(match.group(1)) if match else 0
    else:
        data["in_stock"] = 0

    # 🔹 ТАБЛИЦА ХАРАКТЕРИСТИК
    rows = soup.select('table tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            key = cols[0].get_text(strip=True).rstrip(':')
            value = cols[1].get_text(strip=True)
            # Очищаем ключ для CSV (убираем запрещённые символы)
            key_clean = re.sub(r'[^\w\s]', '', key).strip().replace(' ', '_').lower()
            data[key_clean] = value

    return data


# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    # Читаем список URL
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f" Файл не найден по пути: {INPUT_FILE}")
        print(" Проверь, что файл существует и путь указан верно.")
        return

    print(f" Будет обработано {len(urls)} товаров")
    all_products = []

    for i, url in enumerate(urls, 1):
        print(f" [{i}/{len(urls)}] Парсим: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                product = parse_product_page(response.text, url)
                all_products.append(product)
                print(f" Успешно: {product['name']}")
            else:
                print(f" Страница не найдена (HTTP {response.status_code})")
        except Exception as e:
            print(f" Ошибка при парсинге {url}: {e}")

        # Вежливая пауза — не нагружаем сервер
        time.sleep(1)

    # Сохраняем всё в CSV
    if all_products:
        # Собираем все уникальные ключи (названия столбцов)
        fieldnames = set()
        for p in all_products:
            fieldnames.update(p.keys())
        fieldnames = sorted(fieldnames)

        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_products)

        print(f"\ Все данные сохранены в {OUTPUT_FILE}")
        print(f" Всего товаров: {len(all_products)}")
    else:
        print(" Ни один товар не был успешно распарсен")

    print(" Готово!")


if __name__ == "__main__":
    main()