CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    city TEXT,
    registration_date DATE
);
CREATE TABLE categories(
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);
CREATE TABLE orders(
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE products(
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category_id INTEGER NOT NULL ,
    price INTEGER NOT NULL CHECK (price >=0),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
CREATE TABLE order_items(
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL ,
    product_id INTEGER NOT NULL ,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_the_moment INTEGER CHECK (price_at_the_moment >=0) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
INSERT INTO categories(category_name)
VALUES ('Electronics');
INSERT INTO categories(category_name)
VALUES ('Furniture');
INSERT INTO categories(category_name)
VALUES ('Clothing');
INSERT INTO categories(category_name)
VALUES ('Books');
INSERT INTO categories(category_name)
VALUES ('Sports');
INSERT INTO users(username, email, city, registration_date)
VALUES
('alex_miller', 'alex.miller@example.com', 'Chisinau', '2025-01-15'),
('emma_wilson', 'emma.wilson@example.com', 'Balti', '2025-02-03'),
('daniel_smith', 'daniel.smith@example.com', 'Chisinau', '2025-02-20'),
('olivia_brown', 'olivia.brown@example.com', 'Cahul', '2025-03-11'),
('michael_jones', 'michael.jones@example.com', 'Comrat', '2025-04-07'),
('sophia_davis', 'sophia.davis@example.com', 'Chisinau', '2025-05-19'),
('james_taylor', 'james.taylor@example.com', 'Balti', '2025-06-25'),
('ava_anderson', 'ava.anderson@example.com', 'Orhei', '2025-07-14');
SELECT * FROM users;
INSERT INTO products(product_name, category_id, price, quantity)
VALUES
('Laptop',1,1200,15),
('Wireless Mouse',1,35,50),
('Mechanical Keyboard',1,90,25),
('Office Chair',2,180,12),
('Wooden Desk',2,350,8),
('T-Shirt',3,25,60),
('Jeans',3,70,30),
('Programming in Python',4,45,20),
('Football',5,30,35),
('Headphones',1,80,40);
select * from products;
INSERT INTO orders (order_id, user_id, order_date, status)
VALUES
(1, 1, '2025-08-01', 'completed'),
(2, 2, '2025-08-03', 'completed'),
(3, 3, '2025-08-05', 'shipped'),
(4, 1, '2025-08-10', 'completed'),
(5, 4, '2025-08-12', 'cancelled'),
(6, 5, '2025-08-15', 'completed'),
(7, 6, '2025-08-18', 'processing'),
(8, 7, '2025-08-20', 'completed'),
(9, 8, '2025-08-22', 'shipped'),
(10, 3, '2025-08-25', 'completed'),
(11, 2, '2025-08-27', 'processing'),
(12, 6, '2025-08-30', 'completed');
INSERT INTO order_items
(order_item_id, order_id, product_id, quantity, price_at_the_moment)
VALUES
(1, 1, 1, 1, 1200),
(2, 1, 2, 2, 35),
(3, 2, 6, 3, 25),
(4, 2, 7, 1, 70),
(5, 3, 3, 1, 90),
(6, 3, 10, 1, 80),
(7, 4, 5, 1, 350),
(8, 4, 4, 2, 180),
(9, 5, 9, 1, 30),
(10, 6, 8, 2, 45),
(11, 6, 2, 1, 35),
(12, 7, 1, 1, 1200),
(13, 7, 10, 2, 80),
(14, 8, 7, 2, 70),
(15, 8, 6, 2, 25),
(16, 9, 3, 1, 90),
(17, 9, 2, 1, 35),
(18, 10, 1, 1, 1200),
(19, 10, 3, 1, 90),
(20, 10, 2, 3, 35),
(21, 11, 4, 1, 180),
(22, 11, 5, 1, 350),
(23, 12, 9, 2, 30),
(24, 12, 8, 1, 45);
select *from orders;
select * from order_items;