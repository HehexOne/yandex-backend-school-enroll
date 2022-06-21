from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from db.db_connection import *
from db.db_utils import *
from schema import *
from validators import *

validation_error = Error(code=400, message="Validation Failed").json()
todo_error = Error(code=500, message="TODO").json()
ok_error = Error(code=200, message="OK!").json()
not_found_error = Error(code=404, message="Item not found").json()


app = FastAPI(title="Mega Market Open API",
              version="1.0",
              openapi_version="3.0.0",
              description="Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return PlainTextResponse(validation_error, status_code=400)


@app.post("/imports")
async def imports(shop_unit_import_request: ShopUnitImportRequest):
    if is_valid_shop_unit_import_request(shop_unit_import_request):
        return PlainTextResponse(ok_error, status_code=200)
    else:
        return PlainTextResponse(validation_error, status_code=400)


@app.delete("/delete/{id}")
def delete_by_id(id: str):
    db = RedisUnits()
    unit = db.get(id)
    if not unit:
        return PlainTextResponse(not_found_error, status_code=404)
    if unit.type == ShopUnitType.CATEGORY:
        delete_category(unit.id)
    else:
        delete_category(unit.id)
    return PlainTextResponse(ok_error, status_code=200)


@app.get("/nodes/{id}")
def nodes(id: str):
    db = RedisUnits()
    unit = db.get(id)
    if unit:
        return PlainTextResponse(get_node(unit.id).json(), status_code=200)
    return PlainTextResponse(not_found_error, status_code=404)


@app.get("/sales")
def sales(date: str):
    if is_valid_date(date):
        return PlainTextResponse(ok_error, status_code=200)
    else:
        return PlainTextResponse(validation_error, status_code=400)


@app.get("/node/{id}/statistic")
def node_statistic(id: str, dateStart: str, dateEnd: str):
    return PlainTextResponse(todo_error, status_code=500)
