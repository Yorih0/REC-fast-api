import sqlite3
import hashlib
import os

def Create_Data_Table(folder, name_db, name, password):
    con = sqlite3.connect(f"{folder}/{name_db}.db")
    cursor = con.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            mail TEXT,
            phone TEXT,
            role TEXT NOT NULL,
            hashkey TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Workers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            stage INTEGER NOT NULL,
            description_skills TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            license_plate TEXT NOT NULL,
            region INTEGER NOT NULL,
            description_problem TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,

            worker_id INTEGER,
            description_work TEXT,

            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (worker_id) REFERENCES Workers(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS History_orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            license_plate TEXT NOT NULL,
            region INTEGER NOT NULL,
            description_problem TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,

            worker_id INTEGER,
            description_work TEXT,

            finished_at TEXT NOT NULL,
            cost REAL NOT NULL,
            comment TEXT,

            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (worker_id) REFERENCES Workers(id)
        )
    """)

    con.commit()

    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    cursor.execute("""INSERT INTO Users (role, login, password,phone,mail,hashkey) VALUES (?, ?, ?)""",
                   ("Admin", name, password_hash,"+375 33 000 0000","amdin@admin.com","52423378258435398375830hdkjfsfueskf"))
    con.commit()
    con.close()

if __name__ == "__main__":
    print("Создание базы данных")
    name_db = input("Введите название базы данных: ")
    folder = "Data"

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(os.path.join(folder, name_db + ".db")):
        print("Уже существует")
    else:
        name = input("Введите логин для админа: ")
        password = ""
        while len(password) < 6:
            password = input("Введите пароль для админа: ")
            if len(password) < 6:
                print("Слишком короткий пароль")
        
        Create_Data_Table(folder, name_db, name, password) 
