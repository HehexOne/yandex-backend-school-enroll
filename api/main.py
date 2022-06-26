from datetime import datetime, timedelta
import tarantool
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from api.validators import *
from tarantool_db.tarantool_connection import TarantoolDB

validation_error = Error(code=400, message="Validation Failed").json()
todo_error = Error(code=500, message="TODO").json()
ok_error = Error(code=200, message="OK!").json()
not_found_error = Error(code=404, message="Item not found").json()


def response(content, code):
    return PlainTextResponse(content, code, media_type="application/json")


app = FastAPI(title="Mega Market Open API",
              version="1.0",
              openapi_version="3.0.0",
              description="Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return response(validation_error, 400)


@app.post("/imports")
async def imports(shop_unit_import_request: ShopUnitImportRequest):
    if is_valid_shop_unit_import_request(shop_unit_import_request):
        db = TarantoolDB()
        try:
            return response(db.inserts(shop_unit_import_request.json()), 200)
        except tarantool.DatabaseError as e:
            print(e)
            return response(validation_error, 400)
    else:
        return response(validation_error, 400)


@app.delete("/delete/{id}")
def delete_by_id(id: str):
    db = TarantoolDB()
    try:
        return response(db.delete(id), 200)
    except tarantool.DatabaseError as e:
        return response(not_found_error, 404)


@app.get("/nodes/{id}")
def nodes(id: str):
    db = TarantoolDB()
    try:
        res = db.get_node(id)
        return response(res, 200)
    except tarantool.DatabaseError as e:
        print(e)
        return response(not_found_error, 404)


@app.get("/sales")
def sales(date: str):
    db = TarantoolDB()
    res, val = is_valid_date(date)
    if not res:
        return response(validation_error, 400)
    before_val = datetime.timestamp(val - timedelta(hours=24))
    val = datetime.timestamp(val)
    try:
        res = db.get_sales(val, before_val)
        return response(res, 200)
    except tarantool.DatabaseError as e:
        print(e)
        return response(validation_error, 400)
