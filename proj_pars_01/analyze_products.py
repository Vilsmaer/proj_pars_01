# analyze_products.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === КОНФИГУРАЦИЯ ===
BASE_DIR = r"D:\ANKO\proj_pars_01"
INPUT_FILE = f"{BASE_DIR}\\products.xlsx"
OUTPUT_REPORT = f"{BASE_DIR}\\analysis_report.xlsx"
OUTPUT_CHART = f"{BASE_DIR}\\price_vs_thickness.png"  # Путь к графику

# Читаем Excel
df = pd.read_excel(INPUT_FILE)

print(" Общая статистика:")
print(df.describe())

# 1. Классификация по виду фанеры
print("\n Количество товаров по виду:")
print(df['вид_фанеры'].value_counts())

# 2. Средняя цена по толщине
print("\n Средняя цена по толщине:")
price_by_thickness = df.groupby('толщина')['price'].mean().round(2)
print(price_by_thickness)

# 3. График: Цена vs Толщина
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='толщина', y='price', hue='вид_фанеры', s=100)
plt.title('Цена vs Толщина (по видам фанеры)')
plt.xlabel('Толщина (мм)')
plt.ylabel('Цена (руб)')
plt.grid(True)
plt.savefig(OUTPUT_CHART, dpi=150, bbox_inches='tight')  # Сохраняем в нужную папку
print(f" График сохранён: {OUTPUT_CHART}")
# plt.show()  # Раскомментируй, если хочешь видеть график в интерактивном окне

# 4. Топ-10 самых дорогих товаров
print("\n Топ-10 самых дорогих товаров:")
top_10 = df.nlargest(10, 'price')[['name', 'price', 'толщина', 'формат']]
print(top_10)

# 5. Товары в наличии (больше 20 шт)
in_stock = df[df['in_stock'] > 20]
print(f"\n Товаров в наличии (>20 шт): {len(in_stock)}")
print(in_stock[['name', 'price', 'in_stock']].head())

# 6. Сохраняем отчёт в Excel
with pd.ExcelWriter(OUTPUT_REPORT, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Исходные данные', index=False)
    price_by_thickness.to_excel(writer, sheet_name='Цена по толщине')
    df['вид_фанеры'].value_counts().to_excel(writer, sheet_name='Количество по виду')
    top_10.to_excel(writer, sheet_name='Топ-10 дорогих', index=False)
    in_stock.to_excel(writer, sheet_name='В наличии >20', index=False)

print(f"\n Отчёт сохранён в {OUTPUT_REPORT}")