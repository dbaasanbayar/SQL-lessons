import sqlite3

# 1. Өгөгдлийн сангийн файл үүсгэх (байхгүй бол шинээр үүснэ)
conn = sqlite3.connect('company.db')

# 2. Cursor (курсор) үүсгэх - Энэ нь SQL тушаалыг зөөвөрлөгч юм
cursor = conn.cursor()

# 3. Хүснэгт үүсгэх SQL тушаал
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL
)
''')

# Өөрчлөлтийг хадгалах
conn.commit()
print("Ugugdliin san ba husnegt amjilttai uuslee!")

workers = [
    ('Baasan', 'Engineering', 5000),
    ('Demberel', 'Data Science', 6000),
    ('John', 'Engineering', 4500),
    ('Sara', 'Marketing', 3800)
]

# ? тэмдэгт нь аюулгүй байдлыг хангадаг (SQL Injection-оос сэргийлнэ)
cursor.executemany('INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)', workers)

conn.commit()
print(f"{len(workers)} ajilchnii medeelel hadgalagdlaa.")

import pandas as pd

# Зөвхөн Engineering-ийн ажилчдыг SQL-ээр шүүж авах
query = "SELECT * FROM employees WHERE department = 'Engineering' "

# Pandas-ийн read_sql_query функцээр шууд DataFrame болгох
df = pd.read_sql_query(query, conn)

print("--- Инженерүүдийн жагсаалт (Pandas) ---")
print(df)

# Дундаж цалинг Pandas-аар тооцоолох

print(f"\n Dundaj tsalin: {df['salary'].mean()}")
conn.close()