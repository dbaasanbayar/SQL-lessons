import pandas as pandas
import sqlite3

# 1. Шинэ дата үүсгэх (CSV-ээс биш шууд Питоноор туршиж үзье)
new_data = {
    'name': ['iPhone 16 Pro', 'Google Pixel 9'],
    'price': [1500, 1100],
    'stock': [5, 8]
}
df_new = pandas.DataFrame(new_data)

# 2. Өгөгдлийн санд холбогдох
with sqlite3.connect('automated_store.db') as conn:
    # 'append' ашигласнаар хуучин iPhone 15, Samsung S24 зэрэг нь устахгүй!
    df_new.to_sql('products', conn, if_exists='append', index=False)
    total_df = pandas.read_sql_query("SELECT * FROM products", conn)
    print("--- Өгөгдлийн сан дахь нийт мөрүүд ---")
    print(total_df)
    print(f"\nНийт барааны тоо: {len(total_df)}")
    
    #1. Pandas түвшинд: df.drop_duplicates() ашиглаж цэвэрлэх.
    #2. SQL түвшинд: UNIQUE түлхүүр үг ашиглан нэг нэртэй барааг хоёр удаа оруулахгүй байх тохиргоо хийх.