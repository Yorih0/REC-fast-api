import sqlite3

class HistoryOfOrder:
    def __init__(self, id=None, order_id=None, status=None, timestamp=None, comment=None):
        self.__id = id
        self.__order_id = order_id
        self.__status = status
        self.__timestamp = timestamp
        self.__comment = comment

    # ====== classmethods ======
    @classmethod
    def form_register(cls, row: dict):
        return cls(
            order_id=row.get("order_id"),
            status=row.get("status"),
            timestamp=row.get("timestamp"),
            comment=row.get("comment")
        )

    @classmethod
    def db(cls, row: dict):
        return cls(
            id=row.get("id"),
            order_id=row.get("order_id"),
            status=row.get("status"),
            timestamp=row.get("timestamp"),
            comment=row.get("comment")
        )

    @classmethod
    def by_id(cls, row: dict, file_db):
        history = HistoryOfOrder.Find_history_by_attr("id", row.get("id"), file_db)
        if history and len(history) > 0:
            return cls(
                id=history[0].id,
                order_id=history[0].order_id,
                status=history[0].status,
                timestamp=history[0].timestamp,
                comment=history[0].comment
            )
        return None

    # ====== свойства ======
    @property
    def id(self): return getattr(self, "_HistoryOfOrder__id", None)
    @id.setter
    def id(self, value):
        if value is not None: self.__id = value
        else: raise ValueError("id не может быть пустым")

    @property
    def order_id(self): return getattr(self, "_HistoryOfOrder__order_id", None)
    @order_id.setter
    def order_id(self, value):
        if value is not None: self.__order_id = value
        else: raise ValueError("order_id не может быть пустым")

    @property
    def status(self): return getattr(self, "_HistoryOfOrder__status", None)
    @status.setter
    def status(self, value):
        if value and isinstance(value, str): self.__status = value
        else: raise ValueError("status должен быть строкой")

    @property
    def timestamp(self): return getattr(self, "_HistoryOfOrder__timestamp", None)
    @timestamp.setter
    def timestamp(self, value):
        if value: self.__timestamp = value
        else: raise ValueError("timestamp не может быть пустым")

    @property
    def comment(self): return getattr(self, "_HistoryOfOrder__comment", None)
    @comment.setter
    def comment(self, value):
        if value and isinstance(value, str): self.__comment = value
        else: raise ValueError("comment должен быть строкой")

    # ====== методы информации ======
    def Info(self):
        return {
            "status": self.status,
            "comment": self.comment
        }

    def Info_all(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "status": self.status,
            "timestamp": self.timestamp,
            "comment": self.comment
        }

    # ====== CRUD ======
    def Add_history(self, file_db):
        result = {"status": "error", "message": "Неизвестная ошибка"}
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("""INSERT INTO History_of_orders (order_id, status, timestamp, comment) 
                              VALUES (?, ?, ?, ?)""",
                           (self.order_id, self.status, self.timestamp, self.comment))
            self.id = cursor.lastrowid
            con.commit()
            result["status"] = "success"
            result["message"] = "История добавлена"
            return result
        except sqlite3.Error as e:
            con.rollback()
            result["message"] = f"Ошибка базы данных: {str(e)}"
            return result
        finally:
            con.close()

    def Remove_history(self, file_db):
        result = {"status": "error", "message": "Неизвестная ошибка"}
        if not self.id:
            result["message"] = "ID истории не задан"
            return result
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("DELETE FROM History_of_orders WHERE id = ?", (self.id,))
            con.commit()
            result["status"] = "success"
            result["message"] = "История удалена"
            return result
        except sqlite3.Error as e:
            con.rollback()
            result["message"] = f"Ошибка базы данных: {str(e)}"
            return result
        finally:
            con.close()

    # ====== поиск ======
    @staticmethod
    def Find_history_by_atr(attribute, value, file_db):
        try:
            con = sqlite3.connect(file_db)
            cursor = con.cursor()
            match attribute:
                case "id":
                    query = "SELECT id, order_id, status, timestamp, comment FROM History_of_orders WHERE id = ?"
                case "order_id":
                    query = "SELECT id, order_id, status, timestamp, comment FROM History_of_orders WHERE order_id = ?"
                case "status":
                    query = "SELECT id, order_id, status, timestamp, comment FROM History_of_orders WHERE status = ?"
                case _:
                    return []
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            return [HistoryOfOrder.db({
                "id": row[0],
                "order_id": row[1],
                "status": row[2],
                "timestamp": row[3],
                "comment": row[4]
            }) for row in rows]
        except sqlite3.Error as e:
            print(f"Ошибка при поиске истории: {e}")
            return []
        finally:
            con.close()

    @staticmethod
    def Remove_history_by_atr(attribute, value, file_db):
        try:
            con = sqlite3.connect(file_db)
            cursor = con.cursor()
            match attribute:
                case "id":
                    query = "DELETE FROM History_of_orders WHERE id = ?"
                case "order_id":
                    query = "DELETE FROM History_of_orders WHERE order_id = ?"
                case "status":
                    query = "DELETE FROM History_of_orders WHERE status = ?"
                case _:
                    return 0
            cursor.execute(query, (value,))
            deleted = cursor.rowcount
            con.commit()
            return deleted
        except sqlite3.Error as e:
            print(f"Ошибка при удалении истории: {e}")
            return 0
        finally:
            con.close()
