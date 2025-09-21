# proj_pers_01
Automated collection, analysis, and visualization of data on plywood, OSB, and related materials.

---

# Site Parser fanera-osb.ru

**Automated collection, analysis, and visualization of plywood, OSB, and related materials from the website `fanera-osb.ru `.**

> Without Selenium — works via `requests` + `BeautifulSoup`  
> Fully automated — one run → ready report  
> Ready-made Excel files + graph of price versus thickness

---

## What does the parser do

1. **Data collection**  
   Uses `sitemap.xml to search the URL of product cards → parses the name, price, availability, characteristics (thickness, format, weight, density, etc.).

2. **Structuring**  
   Saves data in:
- `products.xlsx ` is a beautifully formatted table with filters and row fills.
   - `all_products.csv' — raw data to import into BI systems.

3. **Analysis and visualization**  
   Creates a report `analysis_report.xlsx ` c:
- Average price in terms of thickness.
   - Distribution of goods by type.
   - Top 10 most expensive products.
   - Graph "Price vs Thickness" → `price_vs_thickness.png'.

4. **Automation**  
   Launch with a single command:
   ```bash
   python start_pars.py
   ```

---

## Technology

- Python 3.8+
- `requests` + `BeautifulSoup4' — parsing without a browser
- `pandas` + 'openpyxl' — analysis and work with Excel
- `matplotlib' + `seaborn' — charting
- Works on Windows, macOS, Linux

---

## 📥 How to get started

### 1. Clone the repository

```bash
git clone https://github.com/ваш-профиль/fanera-parser.git
cd fanera-parser
``

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the sitemap

Download it `sitemap.xml `from the website `https://fanera-osb.ru/sitemap.xml ` and save it as `Pasted_Text.txt `to the root of the project.

> Or use the attached example.

###4. Run the parser

```bash
python start_pars.py
```

---

## Result

The project folder will display:
- **Scalability** — easy to adapt to other sites.
