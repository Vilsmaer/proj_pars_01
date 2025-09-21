# filtr.py — Фильтруем только URL товаров из sitemap

import re
from bs4 import BeautifulSoup

# Читаем файл sitemap
with open(r"D:\ANKO\proj_pars_01\Pasted_Text.txt", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, "xml")
locs = soup.find_all("loc")

# Паттерны для URL товаров (фанера, OSB и т.д.)
product_url_patterns = [
    r"/fanera/[^/]+/\d+mm[ _\-]\d+x\d+mm",      # /fanera/fbv/18mm-2440x1220mm/
    r"/osb/[^/]+/\d+mm[ _\-]\d+x\d+mm",         # /osb/osb-3-12mm-2440x1220mm/
    r"/dvp-orgalit/\d+mm[ _\-]\d+x\d+mm",       # /dvp-orgalit/3mm-2140x1220mm/
    r"/csp-cementno-struzhechnaya-plita/[^/]+/\d+mm",  # и другие товары
]

product_urls = []

for loc in locs:
    url = loc.get_text(strip=True)
    for pattern in product_url_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            product_urls.append(url)
            break

# Убираем дубликаты
product_urls = list(set(product_urls))

print(f" Найдено {len(product_urls)} URL карточек товаров:")

for i, url in enumerate(product_urls[:10], 1):
    print(f"  {i}. {url}")

# Сохраняем в файл
with open("filtered_product_urls.txt", "w", encoding="utf-8") as f:
    for url in product_urls:
        f.write(url + "\n")

print(f"\n Отфильтрованные URL сохранены в filtered_product_urls.txt")