import sqlite3
from datetime import datetime

class Order:
    def __init__(self, id=None, user_id=None, brand=None, model=None, license_plate=None,
                 region=None, description_problem=None, status=None, created_at=None,
                 worker_id=None, description_work=None):
        self.id = id
        self.user_id = user_id
        self.brand = brand
        self.model = model
        self.license_plate = license_plate
        self.region = region
        self.description_problem = description_problem
        self.status = status
        self.created_at = created_at
        self.worker_id = worker_id
        self.description_work = description_work

    # ====== Создание нового заказа ======
    def create_order(self, file_db):
        if not all([self.user_id, self.brand, self.model, self.license_plate, self.region, self.description_problem]):
            return {"status": "error", "message": "Не заполнены обязательные поля"}

        self.status = self.status or "Обработка"
        self.created_at = self.created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute("""
                INSERT INTO Orders (user_id, brand, model, license_plate, region, description_problem, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.user_id, self.brand, self.model, self.license_plate, self.region,
                  self.description_problem, self.status, self.created_at))
            con.commit()
            self.id = cursor.lastrowid
            return {"status": "success", "message": "Заказ создан", "order_id": self.id}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ====== Получение заказа по ID ======
    @staticmethod
    def get_order_by_id(file_db, order_id):
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM Orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Order(*row)
        finally:
            con.close()

    # ====== Получение всех заказов пользователя ======
    @staticmethod
    def get_orders_by_user_id(file_db, user_id):
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        orders = []
        try:
            cursor.execute("SELECT * FROM Orders WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            for row in rows:
                orders.append(Order(*row))
            return orders
        finally:
            con.close()
            
    @staticmethod
    def get_orders_by_worker_id(file_db, worker_id):
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        orders = []
        try:
            cursor.execute("SELECT * FROM Orders WHERE worker_id = ?", (worker_id,))
            rows = cursor.fetchall()
            for row in rows:
                orders.append(Order(*row))
            return orders
        finally:
            con.close()

    # ====== Получение всех заказов для админа ======
    @staticmethod 
    def get_all_orders(file_db): 
        con = sqlite3.connect(file_db) 
        cursor = con.cursor() 
        orders = [] 
        try: 
            cursor.execute("SELECT * FROM Orders") 
            rows = cursor.fetchall() 
            for row in rows: orders.append(Order(*row)) 
            return orders 
        finally: con.close()

    # ====== Обновление статуса заказа ======
    def update_status(self, file_db, new_status):
        if not self.id:
            return {"status": "error", "message": "ID заказа не задан"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE Orders SET status = ? WHERE id = ?", (new_status, self.id))
            con.commit()
            self.status = new_status
            return {"status": "success", "message": "Статус обновлён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ====== Назначение работника и описание работы ======
    def assign_worker(self, file_db, worker_id, description_work):
        if not self.id:
            return {"status": "error", "message": "ID заказа не задан"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute("UPDATE Orders SET worker_id = ?, description_work = ? WHERE id = ?",
                           (worker_id, description_work, self.id))
            con.commit()
            self.worker_id = worker_id
            self.description_work = description_work
            return {"status": "success", "message": "Работник назначен"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ====== Удаление заказа ======
    def delete_order(self, file_db):
        if not self.id:
            return {"status": "error", "message": "ID заказа не задан"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM Orders WHERE id = ?", (self.id,))
            con.commit()
            return {"status": "success", "message": "Заказ удалён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()
