import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from groq import Groq
import os
from dotenv import load_dotenv

def scrape_montsame():
    url = "https://montsame.mn/mn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Connection Error: {e}")
        return []

    news_list = []
    
    # 1. Сайтын бүх линкүүдийг (<a> таг) олох
    links = soup.find_all('a', href=True)
    
    for link_tag in links:
        url_path = link_tag['href']
        
        # 2. Зөвхөн мэдээний линкүүдийг шүүх (Монцамэ-ийн мэдээ /read/ гэсэн замтай байдаг)
        if '/read/' in url_path:
            title = link_tag.text.strip()
            
            # Гарчиг нь хэт богино бол (жишээ нь 'Дэлгэрэнгүй') алгасах
            if len(title) < 15:
                continue
                
            full_url = url_path if url_path.startswith('http') else "https://montsame.mn" + url_path
            
            news_list.append({
                'title': title,
                'category': 'Мэдээ', # Ангиллыг AI-аар дараа нь хийлгэнэ
                'url': full_url,
                'status': 'raw'
            })
            
    return news_list

# Төслийг ажиллуулах
data = scrape_montsame()
df = pd.DataFrame(data).drop_duplicates(subset=['url'])

if not df.empty:
    print(f"Нийт {len(df)} мэдээ шинэ аргаар оллоо!")
    print(df.head(3)) # Эхний 3-ыг шалгаж харах
    
    with sqlite3.connect('news_analytics.db') as conn:
        df.to_sql('raw_news', conn, if_exists='replace', index=False)
else:
    print("Шинэ аргаар ч дата олдсонгүй. Вэбсайт бүрэн динамик болсон байж магадгүй.")

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"))

def analyze_news_with_ai(title):
    prompt = f"""
    Чи бол мэдээний шинжээч. Дараах мэдээний гарчигт анализ хий: "{title}"
    Хариуг зөвхөн JSON форматаар дараах хэлбэрээр өг:
    {{
        "sentiment": "Эерэг" эсвэл "Сөрөг" эсвэл "Саармаг",
        "category": "Улс төр", "Эдийн засаг", "Спорт" эсвэл "Бусад",
        "summary": "Нэг өгүүлбэрт багтаасан тайлбар"
    }}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant", # Маш хурдан бөгөөд ухаалаг модел
        response_format={"type": "json_object"}
    )
    return chat_completion.choices[0].message.content

# 2. SQL-ээс мэдээгээ унших
with sqlite3.connect('news_analytics.db') as conn:
    df_raw = pd.read_sql_query("SELECT * FROM raw_news LIMIT 5", conn)

    analyzed_data = []
    print("AI Анализ эхэлж байна...")

    for index, row in df_raw.iterrows():
        try:
            ai_result = analyze_news_with_ai(row['title'])
            # AI-ийн хариу (JSON string)-ийг Питоны Dictionary болгох
            import json
            res = json.loads(ai_result)
            
            analyzed_data.append({
                'title': row['title'],
                'category': res['category'],
                'sentiment': res['sentiment'],
                'summary': res['summary'],
                'url': row['url']
            })
            print(f"DONE: {row['title'][:30]}...")
        except Exception as e:
            print(f"Алдаа гарлаа: {e}")

    # 3. LOAD: Анализ хийсэн датаг шинэ хүснэгтэд хадгалах
    df_final = pd.DataFrame(analyzed_data)
    # Хэрэв өмнө нь ижил гарчигтай анализ орсон бол хамгийн сүүлийнхийг нь үлдээх
    df_final = df_final.drop_duplicates(subset=['title'], keep='last')
    df_final.to_sql('analyzed_news', conn, if_exists='append', index=False)

print("\n--- AI Анализ дууслаа! ---")
print(df_final[['title', 'sentiment', 'category']].head())

with sqlite3.connect('news_analytics.db') as conn:
    # SQL JOIN тушаал
    query = """
    SELECT 
        raw_news.title, 
        analyzed_news.sentiment, 
        analyzed_news.category,
        raw_news.url
    FROM raw_news
    INNER JOIN analyzed_news ON raw_news.title = analyzed_news.title
    WHERE analyzed_news.sentiment = 'Саармаг'
    """
    
    joined_df = pd.read_sql_query(query, conn)

print("--- Сөрөг өнгө аястай мэдээнүүд (Joined Data) ---")
print(joined_df)

with sqlite3.connect('news_analytics.db') as conn:
    query = """
    SELECT DISTINCT
        raw_news.title, 
        analyzed_news.sentiment,
        analyzed_news.category,
        raw_news.url
    FROM raw_news INNER JOIN analyzed_news ON raw_news.title = analyzed_news.title
    WHERE (analyzed_news.category = 'Улс төр' AND analyzed_news.sentiment = 'Эерэг') 
    """

    joined_df_p = pd.read_sql_query(query, conn)
    joined_df_p.to_csv('filename.csv', index=False)
print("--- Eyreg and Uls tur өнгө аястай мэдээнүүд (Joined Data) ---")
print(joined_df_p)

