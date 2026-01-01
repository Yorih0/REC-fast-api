import sqlite3
from Class.user import User
from Class.customer import Customer
from Class.worker import Worker
from Class.order import Order
from Class.historyOfOrder import HistoryOfOrder

class SystemData:
    def __init__(self, file_db="Data/REP-1.db"):
        self.file_db = file_db
        self.current_user = None

    # ===== Работа с пользователями =====
    def create_user(self, login, password, password_r, mail, phone):
        user = User.form_register({
            "login": login,
            "password": password,
            "password_r": password_r,
            "mail": mail,
            "phone": phone
        })
        return user.Create_user(self.file_db), user

    def find_user(self, login, password):
        user = User.form_login({"login": login, "password": password})
        result = user.Find_user(self.file_db)
        return result, user

    def delete_user(self, user: User):
        return user.Delete_user(self.file_db)

    # ===== Работа с автомобилями =====
    def add_car(self, user_id, car_model, car_vin):
        car = Customer.form_register({
            "user_id": user_id,
            "car_model": car_model,
            "car_vin": car_vin
        })
        return car.Add_car(self.file_db), car

    def get_cars_by_user(self, user_id):
        return Customer.Get_all_cars_by_user_id(user_id, self.file_db)

    def remove_car(self, car: Customer):
        return car.Remove_car(self.file_db)

    # ===== Работа с работниками =====
    def add_worker(self, user_id, specialization, experience, rating):
        worker = Worker.form_register({
            "user_id": user_id,
            "specialization": specialization,
            "experience": experience,
            "rating": rating
        })
        return worker.Add_worker(self.file_db), worker

    def get_workers_by_attr(self, attr, value):
        return Worker.Get_all_workers_by_atr(attr, value, self.file_db)

    def remove_worker(self, worker: Worker):
        return worker.Remove_worker(self.file_db)

    # ===== Работа с заказами =====
    def add_order(self, customer_id, worker_id, status, description, created_at, finished_at=None):
        order = Order.form_register({
            "customer_id": customer_id,
            "worker_id": worker_id,
            "status": status,
            "description": description,
            "created_at": created_at,
            "finished_at": finished_at
        })
        return order.Add_order(self.file_db), order

    def get_orders_by_user(self, user_id, role):
        return Order.Get_orders_by_user(user_id, role, self.file_db)

    def remove_order(self, order: Order):
        return order.Remove_order(self.file_db)

    def move_orders_to_history(self, user_id, role, comment="Заказ завершён"):
        return Order.Move_orders_to_history_by_user(user_id, role, self.file_db, comment)

    # ===== Работа с историей заказов =====
    def add_history(self, order_id, status, timestamp, comment):
        history = HistoryOfOrder.form_register({
            "order_id": order_id,
            "status": status,
            "timestamp": timestamp,
            "comment": comment
        })
        return history.Add_history(self.file_db), history

    def get_history_by_atr(self, attr, value):
        return HistoryOfOrder.Find_history_by_attr(attr, value, self.file_db)

    def remove_history(self, history: HistoryOfOrder):
        return history.Remove_history(self.file_db)

    def remove_history_by_atr(self, attr, value):
        return HistoryOfOrder.Remove_history_by_attr(attr, value, self.file_db)
