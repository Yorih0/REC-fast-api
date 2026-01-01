# from Class.user import User

# # Путь к существующей базе
# db_path = f"Data/BANK.db"


# # Найти пользователя по логину
# user = User.Find_user_by_atr("login", "new_login_test", db_path)
# if not user:
#     print("Пользователь не найден")
# else:
#     # ----------------- Обновление login -----------------
#     result_login = user.Update_login(db_path, "new_login_test")
#     print("Update login:", result_login)

#     # ----------------- Обновление email -----------------
#     result_mail = user.Update_mail(db_path, "new_email_test@example.com")
#     print("Update mail:", result_mail)

#     # ----------------- Обновление телефона -----------------
#     result_phone = user.Update_phone(db_path, "375291234567")
#     print("Update phone:", result_phone)

#     # ----------------- Обновление роли -----------------
#     result_role = user.Update_role(db_path, "Admin")
#     print("Update role:", result_role)

#     # ----------------- Обновление пароля -----------------
#     result_password = user.Update_password(db_path, "newpassword123", "newpassword123")
#     print("Update password:", result_password)

#     # ----------------- Проверка входа с новым паролем -----------------
#     user.password = "newpassword123"
#     login_check = user.Find_user(db_path)
#     print("Login with new password:", login_check)

#     user = User.Find_user_by_atr("login", "new_login_test", db_path)
#     if user:
#         result_delete = user.Delete_user(db_path)
#         print("Delete user:", result_delete)
#     else:
#         print("Пользователь не найден")


from Class.worker import Worker

db_path = "Data/BANK.db"

def test_worker_crud():
    print("=== CREATE WORKER ===")
    worker = Worker(
        user_id=1,  # ОБЯЗАТЕЛЬНО существующий user_id в Users
        name="Иван Иванов",
        specialization="Электрик",
        stage="5 лет",
        description_skills="Проводка, щиты, розетки"
    )

    res = worker.Create_worker(db_path)
    print(res)
    assert res["status"] == "success"
    assert worker.id is not None

    print("\n=== FIND WORKER ===")
    found = Worker.Find_worker(worker.user_id, db_path)
    assert found is not None
    print(found.Info())

    print("\n=== UPDATE NAME ===")
    res = found.Update_name(db_path, "Иван Петров")
    print(res)
    assert res["status"] == "success"

    print("\n=== UPDATE SPECIALIZATION ===")
    res = found.Update_specialization(db_path, "Сантехник")
    print(res)
    assert res["status"] == "success"

    print("\n=== UPDATE STAGE ===")
    res = found.Update_stage(db_path, "7 лет")
    print(res)
    assert res["status"] == "success"

    print("\n=== UPDATE DESCRIPTION ===")
    res = found.Update_description_skills(db_path, "Трубы, отопление")
    print(res)
    assert res["status"] == "success"

    print("\n=== DELETE WORKER ===")
    res = found.Delete_worker(db_path)
    print(res)
    assert res["status"] == "success"


if __name__ == "__main__":
    test_worker_crud()
