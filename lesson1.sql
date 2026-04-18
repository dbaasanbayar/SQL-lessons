


-- Хүснэгтийн баганууд: id, name, category, price, stock in products

--1. Бүх бүтээгдэхүүний нэр (name) болон үнийг (price) харах.
SELECT name, price
FROM products

-- 2. Үнэ нь 500-аас их бүтээгдэхүүнүүдийг шүүж гаргах.
WHERE price > 500

-- 3. Гаргаж авсан үр дүнгээ үнээр нь ихээс бага руу эрэмбэлэх.
ORDER BY price DESC

SELECT name, price
FROM products
WHERE price > 500
ORDER BY price DESC

-- AND: Хоёр нөхцөл хоёулаа биелэх ёстой.
WHERE category = 'Electronics' AND price < 1000

-- OR: Аль нэг нөхцөл нь биелэхэд хангалттай.
WHERE category = 'Toys' OR price < 10

-- IN: Жагсаалт доторх утгуудын аль нэгтэй таарч байвал. (Python-ий in-тэй ижил)
WHERE category IN ('Electronics', 'Tools', 'Garden')

SELECT * FROM products
WHERE stock > 0 
    AND category IN ('Electronics', 'Tools')


-- 7. SQL-ийн "Текст хайх" : LIKE
-- Үүнд бид % (Wildcard) тэмдэгтийг ашигладаг

-- 'S%': "S"-ээр эхэлсэн ямар ч текст.
-- '%son': "son"-оор төгссөн ямар ч текст (Жишээ нь: Johnson, Wilson).
-- '%iphone%': Дотор нь "iphone" гэдэг үг орсон хаана ч хамаагүй байх текст.

SELECT * FROM products
WHERE name LIKE 'Samsung%';

SELECT * FROM products
WHERE name LIKE '%Samsung';

SELECT * FROM products
WHERE name LIKE '%Samsung%'

-- 8. Null утгатай ажиллах (IS NULL)

SELECT * FROM products
WHERE price IS NULL; -- Үнэ нь тодорхойгүй байгаа бараанууд

SELECT * FROM products
WHERE (name LIKE '%Pro%' AND price > 1000 ) OR category = 'Apple'

-- 9. Өгөгдлийг Нэгтгэх (Aggregations)

-- Үндсэн функцүүд:

COUNT(*): --Нийт мөрийн тоо.
SUM(column) -- Нийт нийлбэр.
AVG(column) -- Дундаж утга.
MAX(column) -- Хамгийн их утга.
MIN(column) -- Хамгийн бага утга.

SELECT COUNT(*) as niit_too, AVG(price) as dundaj_une
FROM products
WHERE category = 'Electronics';
-- (Энд as ашиглан гарах үр дүнгийн баганад "хоч нэр" өгч байна)

-- 10. Хамгийн хүчирхэг хэсэг: GROUP BY

SELECT category, AVG(price) as dundaj_une
FROM products
GROUP BY category;

SELECT product_id, SUM(quantity) as niit_zaragdsan_baraa
FROM sales
GROUP BY product_id
HAVING SUM(quantity) > 10;

-- 11. SQL-ийн "Хамгийн чухал" сэдэв: JOIN (Хүснэгт нэгтгэх)

-- SQL-ийн хамгийн түгээмэл JOIN (INNER JOIN):

SELECT products.name, sales.quantity
FROM sales
JOIN products ON sales.product_id = products.id;

SELECT Users.username, Orders.amount 
FROM Users
JOIN Orders ON Users.id = Orders.user_id
GROUP BY Users.username
HAVING SUM(Orders.amount) > 1000

-- 2. LEFT JOIN

SELECT Users.username, Orders.amount
FROM Users
LEFT JOIN Orders ON Users.id = Orders.user_id;

-- UNION (Хүснэгтүүдийг дээр дээрээс нь өрөх)

SELECT name FROM products
WHERE price > (SELECT AVG(price) FROM products);
-- Дундаж үнээс өндөр үнэтэй бараануудыг олж байна.


-- Өгөгдөл:
-- Students хүснэгт (id, name)
-- Grades хүснэгт (student_id, subject, score)

SELECT Students.name, AVG(Grades.score) as dundaj_onoo 
FROM Students
LEFT JOIN Grades ON Student.id = Grades.student_id
GROUP BY Students.name 
ORDER BY dundaj_onoo DESC





