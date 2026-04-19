import pandas as pd 
import sqlite3

# 1. Өгөгдлийн сантай холбогдох
with sqlite3.connect('automated_store.db') as conn:

# 2. SQL-ээр давхардалгүй нэрсийг шүүж авах
    query = "SELECT DISTINCT name, price, stock FROM products"
    nemeh_df = pd.read_sql_query(query, conn)

# 3. Шүүсэн өгөгдлөө шинэ хүснэгтэд хадгалах
    nemeh_df.to_sql('unique_products', conn, if_exists='replace', index=False)

print("\n--- Давхардалгүй (Unique) барааны жагсаалт ---")
print(nemeh_df)


