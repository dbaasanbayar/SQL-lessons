import sqlite3

database_connect =sqlite3.connect('store.db')
print(f"store uuslee, {database_connect}")

cursor = database_connect.cursor()

schema = cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER,
    stock INTEGER 
)
''')
print(f"schema uuslee, {schema}")
database_connect.commit()
print("Ugugdliin san ba husnegt amjilttai uuslee!")

items = [
    ('Laptop', 1200, 5), 
    ('Mouse', 25, 50), 
    ('Monitor', 300, 0)
         ]
add_items = cursor.executemany('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', items)

database_connect.commit()
print(f"items nemeh {add_items}")
print(f"{len(items)} product medeelel nemegdlee")

import pandas as pandas

query = "SELECT *FROM products WHERE stock > 0"

df = pandas.read_sql_query(query, database_connect)

print("---Product jagsaalt---")
print(df)

database_connect.close()