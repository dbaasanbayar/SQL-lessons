import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# 1. EXTRACT: Вэбсайт руу хандах
url = "https://www.scrapethissite.com/pages/simple/" # Энэ бол сурахад зориулагдсан сайт
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Улс орнуудын нэр болон хүн амын тоог авъя гэж бодъё

countries = []
for row in soup.find_all('div', class_='col-md-4 country'):
    name = row.find('h3', class_='country-name').text.strip()
    capital = row.find('span', class_='country-capital').text.strip()
    population = row.find('span', class_='country-population').text.strip()
    
    countries.append({
        'name': name,
        'capital': capital,
        'population': int(population)
    })

# 2. TRANSFORM: Pandas руу шилжүүлэх
df = pd.DataFrame(countries)

# 3. LOAD: SQL рүү хадгалах
with sqlite3.connect('world_data.db') as conn:
    df.to_sql('countries', conn, if_exists='replace', index=False)
    print("Вэбээс датаг амжилттай авч, SQL-д хадгаллаа!")

    # Шалгалт: Хамгийн их хүн амтай 5 улсыг шүүх
    top_5 = pd.read_sql_query("SELECT * FROM countries ORDER BY population DESC LIMIT 5", conn)
    print("\n--- Хамгийн их хүн амтай 5 улс ---")
    print(top_5)

