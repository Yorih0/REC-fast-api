import sqlite3
import hashlib
import os
import re

class User:
    def __init__(self, id=None, login=None, password=None,mail=None, phone=None, role=None, hashkey=None):
        self.__id = None
        self.__login = None
        self.__password = None
        self.__mail = None
        self.__phone = None
        self.__role = None
        self.__hashkey = None

        if id is not None:
            self.id = id 
        if login is not None: 
            self.login = login 
        if password is not None: 
            self.password = password 
        if mail is not None: 
            self.mail = mail 
        if phone is not None: 
            self.phone = phone 
        if role is not None: 
            self.role = role 
        if hashkey is not None: 
            self.hashkey = hashkey

    @classmethod
    def Login(cls, row: dict):
        return cls(login=row.get("login"), password=row.get("password"))

    @classmethod
    def Register(cls, row: dict):
        return cls(login=row.get("login"),
                   password=row.get("password"),
                   mail=row.get("mail"),
                   phone=row.get("phone"))

    @classmethod
    def DB(cls, row: dict):
        return cls(id=row.get("id"),
                   role=row.get("role"),
                   login=row.get("login"),
                   password=row.get("password"),
                   mail=row.get("mail"),
                   phone=row.get("phone"),
                   hashkey=row.get("hashkey"))

    @classmethod
    def by_hashkey(cls, row: dict, file_db):
        return User.Find_user_by_atr("hashkey", row.get("hashkey"), file_db)

    # ----------------- Свойства -----------------
    @property
    def id(self): return self.__id
    @id.setter
    def id(self, value: int): self.__id = value

    @property
    def role(self): return self.__role
    @role.setter
    def role(self, value: str):
        if value not in ("Admin", "Customer", "Worker"):
            raise ValueError("Нет такой роли")
        self.__role = value

    @property
    def login(self): return self.__login
    @login.setter
    def login(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Логин должен быть непустой строкой")
        self.__login = value

    @property
    def password(self): return self.__password
    @password.setter
    def password(self, value: str):
        if not value or len(value) < 6:
            raise ValueError("Пароль должен быть не менее 6 символов")
        self.__password = value

    @property
    def mail(self): return self.__mail
    @mail.setter
    def mail(self, value: str):
        if not value or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError(f"Некорректный email: {value}")
        self.__mail = value

    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, value: str):
        if not value:
            raise ValueError("Телефон не может быть пустым")
        digits = ''.join(filter(str.isdigit, value))
        if not re.fullmatch(r'(375|80)(25|29|33|44)\d{7}', digits):
            raise ValueError("Некорректный белорусский телефон")
        self.__phone = digits

    @property
    def hashkey(self): return self.__hashkey
    @hashkey.setter
    def hashkey(self, value): self.__hashkey = value

    # ----------------- Информация о пользователе -----------------
    def Info(self):
        return {"role": self.role, "login": self.login, "mail": self.mail, "phone": self.phone}

    def Info_all(self):
        return {"id": self.id, "role": self.role, "login": self.login,"password": self.password, "mail": self.mail, "phone": self.phone, "hashkey": self.hashkey}

    # ----------------- Создание пользователя -----------------
    def Create_user(self, file_db):
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            for field, value, msg in [("login", self.login, "Такой логин уже существует"),
                                      ("mail", self.mail, "Такая почта уже зарегистрирована"),
                                      ("phone", self.phone, "Такой телефон уже зарегистрирован")]:
                cursor.execute(f"SELECT id FROM Users WHERE {field} = ?", (value,))
                if cursor.fetchone():
                    con.rollback()
                    return {"status": "error", "message": msg}

            self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
            self.hashkey = hashlib.sha256(os.urandom(32)).hexdigest() 

            cursor.execute(
                """INSERT INTO Users (role, login, password, mail, phone, hashkey)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                ("Customer", self.login, self.password, self.mail, self.phone, self.hashkey)
            )
            self.id = cursor.lastrowid
            con.commit()
            return {"status": "success", "message": "Пользователь успешно зарегистрирован"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ----------------- Поиск пользователя -----------------
    def Find_user(self, file_db):
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT id, role, login, password, mail, phone, hashkey FROM Users WHERE login = ?",
                (self.login,)
            )
            row = cursor.fetchone()
            if not row:
                return {"status": "error", "message": "Логин не найден или неверный пароль"}

            user_id, role, login, password_db, mail, phone, hashkey = row

            if not hashkey:
                return {"status": "error", "message": "Повреждённые данные пользователя"}

            self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
            if self.password != password_db:
                return {"status": "error", "message": "Неверный пароль"}

            self.id, self.role, self.login, self.mail, self.phone, self.hashkey = \
                user_id, role, login, mail, phone, hashkey

            return {"status": "success", "message": "Вход выполнен"}
        finally:
            con.close()
    # ----------------- Поиск по атрибуту -----------------
    @staticmethod
    def Find_user_by_atr(attribute, value, file_db):
        if attribute not in ("hashkey", "login", "mail", "phone"):
            return None
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute(
                f"SELECT id, role, login, password, mail, phone, hashkey FROM Users WHERE {attribute} = ?",
                (value,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return User.DB({
                "id": row[0], "role": row[1], "login": row[2], "password": row[3],
                "mail": row[4], "phone": row[5], "hashkey": row[6]
            })
        finally:
            con.close()
    # ----------------- Обновление login -----------------
    def Update_login(self, file_db, new_login):
        if not self.id:
            return {"status": "error", "message": "ID пользователя не задан"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("SELECT id FROM Users WHERE login = ? AND id != ?", (new_login, self.id))
            if cursor.fetchone():
                return {"status": "error", "message": "Такой логин уже существует"}
            cursor.execute("UPDATE Users SET login = ? WHERE id = ?", (new_login, self.id))
            con.commit()
            self.login = new_login
            return {"status": "success", "message": "Логин успешно обновлён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()


    # ----------------- Обновление mail -----------------
    def Update_mail(self, file_db, new_mail):
        if not self.id:
            return {"status": "error", "message": "ID пользователя не задан"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("SELECT id FROM Users WHERE mail = ? AND id != ?", (new_mail, self.id))
            if cursor.fetchone():
                return {"status": "error", "message": "Такая почта уже зарегистрирована"}
            cursor.execute("UPDATE Users SET mail = ? WHERE id = ?", (new_mail, self.id))
            con.commit()
            self.mail = new_mail
            return {"status": "success", "message": "Email успешно обновлён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()


    # ----------------- Обновление phone -----------------
    def Update_phone(self, file_db, new_phone):
        if not self.id:
            return {"status": "error", "message": "ID пользователя не задан"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("SELECT id FROM Users WHERE phone = ? AND id != ?", (new_phone, self.id))
            if cursor.fetchone():
                return {"status": "error", "message": "Такой телефон уже зарегистрирован"}
            cursor.execute("UPDATE Users SET phone = ? WHERE id = ?", (new_phone, self.id))
            con.commit()
            self.phone = new_phone
            return {"status": "success", "message": "Телефон успешно обновлён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()


    # ----------------- Обновление role -----------------
    def Update_role(self, file_db, new_role):
        if not self.id:
            return {"status": "error", "message": "ID пользователя не задан"}
        if new_role not in ("Admin", "Customer", "Worker"):
            return {"status": "error", "message": "Неверная роль"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("UPDATE Users SET role = ? WHERE id = ?", (new_role, self.id))
            con.commit()
            self.role = new_role
            return {"status": "success", "message": "Роль успешно обновлена"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()


    # ----------------- Обновление пароля -----------------
    def Update_password(self, file_db, new_password, new_password_r):
        if not self.id:
            return {"status": "error", "message": "ID пользователя не задан"}
        if new_password != new_password_r:
            return {"status": "error", "message": "Пароли не совпадают"}
        if len(new_password) < 6:
            return {"status": "error", "message": "Пароль должен быть не менее 6 символов"}

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
            self.hashkey = hashlib.sha256(os.urandom(32)).hexdigest() 

            cursor.execute("UPDATE Users SET password = ?, hashkey = ? WHERE id = ?", 
                        (self.password, self.hashkey, self.id))
            con.commit()
            return {"status": "success", "message": "Пароль успешно изменён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ----------------- Удаление пользователя -----------------
    def Delete_user(self, file_db):
        if not self.id:
            return {"status": "error", "message": "ID пользователя не задан"}

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("DELETE FROM Users WHERE id = ?", (self.id,))
            con.commit()
            return {"status": "success", "message": "Пользователь удалён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()


