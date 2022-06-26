import tarantool
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from db.db_utils import *
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
            res = db.inserts(shop_unit_import_request.json())
            return response(res[0], 200)
        except tarantool.DatabaseError as e:
            return response(validation_error, 400)
    else:
        return response(validation_error, 400)


@app.delete("/delete/{id}")
def delete_by_id(id: str):
    db = RedisUnits()
    unit = db.get(id)
    if not unit:
        return response(not_found_error, 404)
    if unit.type == ShopUnitType.CATEGORY:
        delete_category(unit.id)
    else:
        delete_category(unit.id)
    return response(ok_error, 200)


@app.get("/nodes/{id}")
def nodes(id: str):
    db = RedisUnits()
    unit = db.get(id)
    if unit:
        return response(get_node(unit.id).json(), 200)
    return response(not_found_error, 404)


@app.get("/sales")
def sales(date: str):
    if is_valid_date(date):
        return response(json.dumps({"items": get_sales(date)}), 200)
    else:
        return response(validation_error, 400)
