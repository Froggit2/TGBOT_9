import sqlite3

# Подключение к базе данных
connection_prod = sqlite3.connect('product_database.dp')
cursor_prod = connection_prod.cursor()

connection_users = sqlite3.connect('users_database.dp')
cursor_users = connection_users.cursor()

# Создание таблицы, если она не существует
cursor_prod.execute('''
CREATE TABLE IF NOT EXISTS Products
(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER
)
''')

cursor_users.execute('''
CREATE TABLE IF NOT EXISTS Users
(
    id INT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
)
''')


def get_all_products(id_prod, title_prod, description_prod, price_prod):
    # Проверяем, существует ли уже продукт с данным id
    cursor_prod.execute("SELECT * FROM Products WHERE id=?", (id_prod,))
    check_prod = cursor_prod.fetchone()
    # Если продукта нет, добавляем( чисто чтобы затестить)
    if check_prod is None:
        cursor_prod.execute(
            "INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)",
            (id_prod, title_prod, description_prod, price_prod))
        connection_prod.commit()  # фиксируем
    # Возвращаем ВСЕ продукты из базы данных
    cursor_prod.execute("SELECT * FROM Products")
    products = cursor_prod.fetchall()
    return products


def add_users(username, email, age):
    check_user = cursor_users.execute("SELECT * FROM Users WHERE email=?", (email,)).fetchone()
    print(check_user)
    if check_user is None:
        cursor_users.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                            (username, email, age, 1000))
        connection_users.commit()
    else:
        return False


def is_included(username):
    check_user = cursor_users.execute(f"SELECT * FROM Users WHERE username={username}").fetchone()
    if check_user is None:
        return False
    else:
        return True


# вызов функции
all_products_1 = get_all_products(1, 'Product A', 'Description A', 200)
# all_products_2 = get_all_products(2, 'Product B', 'Description B', 100)
# print(all_products_2)

# Закрываем бд
connection_prod.close()