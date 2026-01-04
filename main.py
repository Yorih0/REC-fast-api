from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
import uvicorn
import os
from datetime import datetime
from Class.user import User
from Class.order import Order as Orders
from Class.worker import Worker
import random

FILE_DB = f"Data/BANK.db"
FOLDER = "page"

app = FastAPI()
app.mount("/css", StaticFiles(directory=f"{FOLDER}/css"), name="css")
app.mount("/js", StaticFiles(directory=f"{FOLDER}/js"), name="js")
app.mount("/png", StaticFiles(directory=f"{FOLDER}/png"), name="png")


def render_page(name_page: str): 
    path = os.path.join(FOLDER, f"{name_page}.html") 
    if not os.path.exists(path): 
        return HTMLResponse("<h1>Страница не найдена</h1>", status_code=404) 
    with open(path, "r", encoding="utf-8") as f: 
        return HTMLResponse(f.read())

#Get
@app.get("/", response_class=HTMLResponse)
def main_page():
    return render_page("main")
    
@app.get("/login", response_class=HTMLResponse)
def login_page():
     return render_page("login")
     
@app.get("/register", response_class=HTMLResponse)
def register_page():
     return render_page("register")

@app.get("/order", response_class=HTMLResponse)
def order_page():
     return render_page("order")

@app.get("/worker", response_class=HTMLResponse)
def worker_page():
      return render_page("worker")

@app.get("/profile_user", response_class=HTMLResponse)
def profile_page():
      return render_page("profile_user")

@app.get("/profile_admin", response_class=HTMLResponse)
def profile_page():
      return render_page("profile_admin")

@app.get("/profile_worker", response_class=HTMLResponse)
def profile_page():
      return render_page("profile_worker")

#Post
@app.post("/Login")
async def login(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"message": "Пустое тело запроса"}, status_code=400)

    login = data.get("login")
    password = data.get("password")
    print(login, password)
    try:
        user = User.Login(data)
        response = user.Find_user(FILE_DB)

        if response["status"] == "error":
            return JSONResponse({"message": "Неверный логин или пароль"}, status_code=401) 
        else:
            return JSONResponse({
                    "status": "success",
                    "message": "Вход успешна",
                    "hashkey": user.hashkey
                }, status_code=200)
    except ValueError as e:
            return JSONResponse({"message": str(e)}, status_code=401) 



@app.post("/Register")
async def Register(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"message": "Пустое тело запроса"}, status_code=400)

    login = data.get("login")
    password = data.get("password")
    password_r = data.get("password_r")
    mail = data.get("mail")
    phone = data.get("phone")
    print("INFO")
    print(login)
    print(password)
    print(password_r)
    print(mail)
    print(phone)

    if password != password_r:
        return JSONResponse({"message": "Пароли не совпадают"}, status_code=400)
    else:
        try:
            user = User.Register(data)
            response = user.Create_user(FILE_DB)
            if response["status"] == "error":
                return JSONResponse({"message": response["message"]}, status_code=401) 
            else: 
                return JSONResponse({
                        "status": "success",
                        "message": "Регистрация успешна",
                        "hashkey": user.hashkey
                    }, status_code=200)
        except ValueError as e:
            return JSONResponse({"message": str(e)}, status_code=401)



@app.post("/Order")
async def Order(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"message": "Пустое тело запроса"}, status_code=400)

    hashkey = data.get("hashkey")
    brand = data.get("brand")
    model = data.get("model")
    license_plate = data.get("license_plate")
    region = data.get("region")
    problem = data.get("problem")
    description_problem = data.get("description_problem")
    status = "Обработка"
    create_at_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("INFO")
    print(hashkey)
    print(brand)
    print(model)
    print(problem)  
    if not all([hashkey, brand, model, license_plate, region, description_problem]):
        return JSONResponse({"message": "Не заполнены обязательные поля"}, status_code=400)
    try:
        user = User.by_hashkey({"hashkey": hashkey}, FILE_DB)
        if not user:
            return JSONResponse({"message": "Пользователь не найден"}, status_code=401)

        order = Orders(
            user_id=(user.id),
            brand=brand,
            model=model,
            license_plate=license_plate,
            region=region,
            description_problem=description_problem
        )

        result = order.create_order(FILE_DB)
        if result["status"] == "success":
            return JSONResponse({"message": "Заказ успешно создан", "order_id": result["order_id"]}, status_code=200)
        else:
            return JSONResponse({"message": result["message"]}, status_code=400)

    except ValueError as e:
        return JSONResponse({"message": str(e)}, status_code=401)



@app.post("/Profile")
async def profile(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"message": "Пустое тело запроса"}, status_code=400)

    hashkey = data.get("hashkey")
    if not hashkey:
        return JSONResponse({"message": "hashkey отсутствует"}, status_code=400)

    try:
        user = User.by_hashkey({"hashkey": hashkey}, FILE_DB)
        if not user:
            return JSONResponse({"message": "Пользователь не найден"}, status_code=401)
        return JSONResponse({
            "status": "success",
            "type": user.role
        }, status_code=200)
        
    except ValueError as e:
        return JSONResponse({"message": str(e)}, status_code=401)


@app.post("/load_profile_user")
async def load_profile(request:Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"message": "Пустое тело запроса"}, status_code=400)
    try :
        user_h = User.by_hashkey(data,FILE_DB)
        orders = Orders.get_orders_by_user_id(FILE_DB,user_h.id)
        response = {"message": "Загрузка",
                    "login": user_h.login,
                    "email":user_h.mail,
                    "phone": user_h.phone,
                    "role":user_h.role,
                    "count":len(orders),
                    "orders":{}
                    }
        id_count = 1
        for ord in orders:
            worker = Worker.Find_worker_by_user_id(ord.worker_id,FILE_DB)
            if worker: 
                worker_name = worker.name 
            else: 
                worker_name = "Не назначен"
            if ord.description_work in (None, "None"): 
                description_work = "Ничего не делали"
            else:
                description_work = ord.description_work
            response["orders"][f"order-{id_count}"] = {
                "id" : ord.id,
                "brand" : ord.brand,
                "model" : ord.model,
                "license_plate" : ord.license_plate,
                "region" : ord.region,
                "description_problem" : ord.description_problem,
                "status" : ord.status,
                "worker_id" : worker_name,
                "description_work" : description_work
            }
            id_count+=1
        try:
            return JSONResponse(response, status_code=200)
        except ValueError as e:
            return JSONResponse({"message": str(e)}, status_code=401)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=401)
    


@app.post("/load_profile_admin")
async def load_profile(request:Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"message": "Пустое тело запроса"}, status_code=400)
    
    try:
        user_a = User.by_hashkey(data,FILE_DB)
        if(user_a.role != "Admin"):
            return JSONResponse({"message": "Нет Доступа"}, status_code=400)
        
        orders = Orders.get_all_orders(FILE_DB)

        response = {"message": "Загрузка",
                    "role":user_a.role,
                    "count":len(orders),
                    "orders":{}
                    }
        id_count = 1
        for ord in orders:
            worker = Worker.Find_worker_by_user_id(ord.worker_id,FILE_DB)
            if worker: 
                worker_name = worker.name 
            else: 
                worker_name = "Не назначен"
            if ord.description_work in (None, "None"): 
                description_work = "Ничего не делали"
            else:
                description_work = ord.description_work
            response["orders"][f"order-{id_count}"] = {
                "id" : ord.id,
                "brand" : ord.brand,
                "model" : ord.model,
                "license_plate" : ord.license_plate,
                "region" : ord.region,
                "description_problem" : ord.description_problem,
                "status" : ord.status,
                "worker_id" : worker_name,
                "description_work" : description_work
            }
            id_count+=1
        try:
            return JSONResponse(response, status_code=200)
        except ValueError as e:
            return JSONResponse({"message": str(e)}, status_code=401)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=401)






if __name__ == "__main__":
    uvicorn.run("main:app",reload = True)