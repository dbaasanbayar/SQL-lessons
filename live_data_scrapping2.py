import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# 1. EXTRACT: Вэбсайт руу хандах

url = "https://www.scrapethissite.com/pages/forms/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

teams = []

for row in soup.find_all('tr', class_='team'):
    name = row.find('td', class_='name').text.strip()
    year = row.find('td', class_='year').text.strip()
    wins = row.find('td', class_='wins').text.strip()
    losses = row.find('td', class_='losses').text.strip()

    teams.append({
        'name': name,
        'year': year,
        'wins': wins,
        'losses': losses
    })
    
if not teams: 
    print("Дата олдсонгүй! Вэбсайтын бүтэц өөрчлөгдсөн эсвэл буруу хаяг байна.")
else :
    df =pd.DataFrame(teams)


with sqlite3.connect('hockey_stats.db') as conn:
    df.to_sql('teams', conn, if_exists='append', index=False)
    print("Вэбээс датаг амжилттай авч, SQL-д хадгаллаа!")

    query = "SELECT * FROM teams ORDER BY wins DESC LIMIT 10"
    top_teams = pd.read_sql_query(query, conn)

    print("\n--- Хамгийн их хожилтой 10 баг ---")
    print(top_teams)

    