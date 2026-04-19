import pandas as pandas
import sqlite3

# 3. LOAD: SQL рүү хадгалах
# 'with' ашиглавал conn.close() гараар бичих шаардлагагүй, файл гэмтэх нь багасна
with sqlite3.connect('automated_store.db') as conn:

# 1. EXTRACT: CSV файлыг унших
    df = pandas.read_csv('data.csv')

# 2. TRANSFORM: Өгөгдлийг цэвэрлэх
# Үнэ (price) хэсэгт тоо биш утга байвал (жишээ нь 'free') 0 болгох
df['price'] = pandas.to_numeric(df['price'], errors='coerce').fillna(0)

# Агуулахын үлдэгдэл (stock) хоосон байвал 0 болгох
df['stock'] = df['stock'].fillna(0)

print("--- Цэвэрлэсэн өгөгдөл ---")
print(df)

# Pandas-ийн 'to_sql' функц нь хүснэгтийг автоматаар үүсгэж датаг хадгалдаг!
# if_exists='replace' гэвэл хуучин хүснэгтийг устгаад шинээр үүсгэнэ
df.to_sql('products', conn, if_exists='replace', index=False)

print("\nДата амжилттай SQL рүү шилжлээ!")

# Шалгалт: SQL-ээс буцааж унших
query = "SELECT * FROM products WHERE name LIKE 'iPhone%' OR name LIKE 'Samsung%' "
check_df = pandas.read_sql_query(query, conn)

print("\n--- Шүүсэн өгөгдөл ---")
print(check_df)
