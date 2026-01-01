import sqlite3

class Customer:
    def __init__(self, id=None, user_id=None, car_model=None, car_vin=None):
        self.__id = id
        self.__user_id = user_id
        self.__car_model = car_model
        self.__car_vin = car_vin

    # ====== classmethods для разных источников ======
    @classmethod
    def form_register(cls, row: dict):
        return cls(
            user_id=row.get("user_id"),
            car_model=row.get("car_model"),
            car_vin=row.get("car_vin")
        )

    @classmethod
    def db(cls, row: dict):
        return cls(
            id=row.get("id"),
            user_id=row.get("user_id"),
            car_model=row.get("car_model"),
            car_vin=row.get("car_vin")
        )

    @classmethod
    def by_id(cls, row: dict, file_db):
        customer = Customer.Find_car_by_atr("id", row.get("id"), file_db)
        if customer:
            return cls(
                id=customer.id,
                user_id=customer.user_id,
                car_model=customer.car_model,
                car_vin=customer.car_vin
            )
        return None

    # ====== свойства ======
    @property
    def id(self): return getattr(self, "_Customer__id", None)
    @id.setter
    def id(self, value):
        if value is not None:
            self.__id = value
        else:
            raise ValueError("id не может быть пустым")

    @property
    def user_id(self): return getattr(self, "_Customer__user_id", None)
    @user_id.setter
    def user_id(self, value):
        if value is not None:
            self.__user_id = value
        else:
            raise ValueError("user_id не может быть пустым")

    @property
    def car_model(self): return getattr(self, "_Customer__car_model", None)
    @car_model.setter
    def car_model(self, value):
        if value and isinstance(value, str):
            self.__car_model = value
        else:
            raise ValueError("car_model должен быть строкой")

    @property
    def car_vin(self): return getattr(self, "_Customer__car_vin", None)
    @car_vin.setter
    def car_vin(self, value):
        if value and isinstance(value, str):
            self.__car_vin = value
        else:
            raise ValueError("car_vin должен быть строкой")

    # ====== методы информации ======
    def Info(self):
        return {
            "car_model": self.car_model,
            "car_vin": self.car_vin
        }

    def Info_all(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "car_model": self.car_model,
            "car_vin": self.car_vin
        }

    # ====== CRUD ======
    def Add_car(self, file_db):
        result = {"status": "error", "message": "Неизвестная ошибка"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute(
                "INSERT INTO Customers (user_id, car_model, car_vin) VALUES (?, ?, ?)",
                (self.user_id, self.car_model, self.car_vin)
            )
            self.id = cursor.lastrowid
            con.commit()
            result["status"] = "success"
            result["message"] = "Автомобиль добавлен"
            return result
        except sqlite3.Error as e:
            con.rollback()
            result["message"] = f"Ошибка базы данных: {str(e)}"
            return result
        finally:
            con.close()

    def Remove_car(self, file_db):
        result = {"status": "error", "message": "Неизвестная ошибка"}
        if not self.id:
            result["message"] = "ID автомобиля не задан"
            return result
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("DELETE FROM Customers WHERE id = ?", (self.id,))
            con.commit()
            result["status"] = "success"
            result["message"] = "Автомобиль удалён"
            return result
        except sqlite3.Error as e:
            con.rollback()
            result["message"] = f"Ошибка базы данных: {str(e)}"
            return result
        finally:
            con.close()

    def Update_car(self, file_db):
        result = {"status": "error", "message": "Неизвестная ошибка"}
        if not self.id:
            result["message"] = "ID автомобиля не задан"
            return result
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("""
                UPDATE Customers
                SET user_id = ?, car_model = ?, car_vin = ?
                WHERE id = ?
            """, (self.user_id, self.car_model, self.car_vin, self.id))
            con.commit()
            result["status"] = "success"
            result["message"] = "Данные автомобиля обновлены"
            return result
        except sqlite3.Error as e:
            con.rollback()
            result["message"] = f"Ошибка базы данных: {str(e)}"
            return result
        finally:
            con.close()

    # ====== поиск ======
    @staticmethod
    def Find_car_by_atr(attribute, value, file_db):
        try:
            con = sqlite3.connect(file_db)
            cursor = con.cursor()
            match attribute:
                case "id":
                    query = "SELECT id, user_id, car_model, car_vin FROM Customers WHERE id = ?"
                case "user_id":
                    query = "SELECT id, user_id, car_model, car_vin FROM Customers WHERE user_id = ?"
                case "car_model":
                    query = "SELECT id, user_id, car_model, car_vin FROM Customers WHERE car_model = ?"
                case "car_vin":
                    query = "SELECT id, user_id, car_model, car_vin FROM Customers WHERE car_vin = ?"
                case _:
                    return None
            cursor.execute(query, (value,))
            row = cursor.fetchone()
            if row is None:
                return None
            car_data = {
                "id": row[0],
                "user_id": row[1],
                "car_model": row[2],
                "car_vin": row[3]
            }
            return Customer.db(car_data)
        except sqlite3.Error as e:
            print(f"Ошибка при поиске автомобиля: {e}")
            return None
        finally:
            con.close()

    @staticmethod
    def Get_all_cars_by_user_id(user_id, file_db):
        try:
            con = sqlite3.connect(file_db)
            cursor = con.cursor()
            cursor.execute(
                "SELECT id, user_id, car_model, car_vin FROM Customers WHERE user_id = ?",
                (user_id,)
            )
            rows = cursor.fetchall()
            if not rows:
                return []
            return [Customer.db({
                "id": row[0],
                "user_id": row[1],
                "car_model": row[2],
                "car_vin": row[3]
            }) for row in rows]
        except sqlite3.Error as e:
            print(f"Ошибка при получении автомобилей: {e}")
            return []
        finally:
            con.close()

    @staticmethod
    def Remove_all_cars_by_user_id(user_id, file_db):
        try:
            con = sqlite3.connect(file_db)
            cursor = con.cursor()
            cursor.execute("DELETE FROM Customers WHERE user_id = ?", (user_id,))
            con.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Ошибка при удалении автомобилей: {e}")
            return 0
        finally:
            con.close()
