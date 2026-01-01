import sqlite3

class Worker:
    def __init__(self, id=None, user_id=None,status = None,name=None,specialization=None, stage=None, description_skills=None):
        self.__id = None
        self.__user_id = None
        self.__status = None
        self.__name = None
        self.__specialization = None
        self.__stage = None
        self.__description_skills = None

        if id is not None:
            self.id = id 
        if user_id is not None: 
            self.user_id = user_id 
        if name is not None: 
            self.name = name 
        if specialization is not None: 
            self.specialization = specialization 
        if stage is not None: 
            self.stage = stage 
        if description_skills is not None: 
            self.description_skills = description_skills

    @classmethod
    def Register(cls, row: dict):
        return cls(
            login=row.get("user_id"),
            password=row.get("name"),
            password_r=row.get("password_r"),
            mail=row.get("mail"),
            phone=row.get("phone"))

    @classmethod
    def DB(cls, row: dict):
        return cls(
            id=row.get("id"),
            role=row.get("role"),
            login=row.get("login"),
            password=row.get("password"),
            mail=row.get("mail"),
            phone=row.get("phone"),
            hashkey=row.get("hashkey"))

    # ----------------- Свойства -----------------
    @property
    def id(self): return self.__id
    @id.setter
    def id(self, value): self.__id = value

    @property
    def user_id(self): return self.__user_id
    @user_id.setter
    def user_id(self, value): self.__user_id = value

    @property
    def name(self): return self.__name
    @name.setter
    def name(self, value): self.__name = value

    @property
    def specialization(self): return self.__specialization
    @specialization.setter
    def specialization(self, value): self.__specialization = value

    @property
    def stage(self): return self.__stage
    @stage.setter
    def stage(self, value): self.__stage = value

    @property
    def description_skills(self): return self.__description_skills
    @description_skills.setter
    def description_skills(self, value): self.__description_skills = value

    # ----------------- Информация -----------------
    def Info(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "specialization": self.specialization,
            "stage": self.stage,
            "description_skills": self.description_skills
        }

    # ----------------- Создание -----------------
    def Create_worker(self, file_db):
        if not self.user_id:
            return {"status": "error", "message": "user_id не задан"}

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("""
                INSERT INTO Workers (user_id, name, specialization, stage, description_skills)
                VALUES (?, ?, ?, ?, ?)
            """, (self.user_id, self.name, self.specialization,
                  self.stage, self.description_skills))
            self.id = cursor.lastrowid
            con.commit()
            return {"status": "success", "message": "Работник добавлен"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ----------------- Поиск по user_id -----------------
    @staticmethod
    def Find_worker(user_id, file_db):
        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute("""
                SELECT id, user_id, name, specialization, stage, description_skills
                FROM Workers WHERE user_id = ?
            """, (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Worker(
                id=row[0],
                user_id=row[1],
                name=row[2],
                specialization=row[3],
                stage=row[4],
                description_skills=row[5]
            )
        finally:
            con.close()

    # ----------------- Поиск по атрибуту -----------------
    @staticmethod
    def Find_worker_by_atr(attribute, value, file_db):
        if attribute not in ("id", "user_id", "name", "specialization"):
            return None

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            cursor.execute(
                f"SELECT id, user_id, name, specialization, stage, description_skills "
                f"FROM Workers WHERE {attribute} = ?",
                (value,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return Worker(
                id=row[0],
                user_id=row[1],
                name=row[2],
                specialization=row[3],
                stage=row[4],
                description_skills=row[5]
            )
        finally:
            con.close()

    # ----------------- Обновление name -----------------
    def Update_name(self, file_db, new_name):
        return self.__update_field(file_db, "name", new_name)

    # ----------------- Обновление specialization -----------------
    def Update_specialization(self, file_db, new_specialization):
        return self.__update_field(file_db, "specialization", new_specialization)

    # ----------------- Обновление stage -----------------
    def Update_stage(self, file_db, new_stage):
        return self.__update_field(file_db, "stage", new_stage)

    # ----------------- Обновление description_skills -----------------
    def Update_description_skills(self, file_db, new_description):
        return self.__update_field(file_db, "description_skills", new_description)

    # ----------------- Универсальный update -----------------
    def __update_field(self, file_db, field, value):
        if not self.id:
            return {"status": "error", "message": "ID работника не задан"}

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute(
                f"UPDATE Workers SET {field} = ? WHERE id = ?",
                (value, self.id)
            )
            con.commit()
            setattr(self, field, value)
            return {"status": "success", "message": f"{field} обновлено"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()

    # ----------------- Удаление -----------------
    def Delete_worker(self, file_db):
        if not self.id:
            return {"status": "error", "message": "ID работника не задан"}

        con = sqlite3.connect(file_db)
        cursor = con.cursor()
        try:
            con.execute("BEGIN TRANSACTION")
            cursor.execute("DELETE FROM Workers WHERE id = ?", (self.id,))
            if cursor.rowcount == 0:
                con.rollback()
                return {"status": "error", "message": "Работник не найден"}
            con.commit()
            return {"status": "success", "message": "Работник удалён"}
        except sqlite3.Error as e:
            con.rollback()
            return {"status": "error", "message": f"Ошибка базы данных: {e}"}
        finally:
            con.close()
