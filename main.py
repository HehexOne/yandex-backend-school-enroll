from datetime import datetime
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from schema import *

validation_error = Error(code=400, message="Validation Failed").json()
todo_error = Error(code=500, message="TODO").json()
ok_error = Error(code=200, message="OK!").json()


def is_valid_date(mts):
    try:
        datetime.strptime(mts, '%Y-%m-%dT%H:%M:%S.%f%z')
        return True
    except ValueError:
        return False


def is_valid_price(sui: ShopUnitImport):
    if (not sui.price and sui.type == ShopUnitType.CATEGORY) or\
            (sui.type == ShopUnitType.OFFER and sui.price and (0 <= sui.price <= 9223372036854775807)):
        return True
    else:
        return False


def is_valid_shop_unit_import_request(suir: ShopUnitImportRequest):
    if (not all(map(is_valid_price, suir.items))) or (not is_valid_date(suir.updateDate)) or\
            len(suir.items) != len(set(map(lambda item: item.id, suir.items))):
        return False
    else:
        return True


app = FastAPI(title="Mega Market Open API",
              version="1.0",
              openapi_version="3.0.0",
              description="Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(validation_error, status_code=400)


@app.post("/imports")
async def imports(shop_unit_import_request: ShopUnitImportRequest):
    if is_valid_shop_unit_import_request(shop_unit_import_request):
        return PlainTextResponse(ok_error, status_code=200)
    else:
        return PlainTextResponse(validation_error, status_code=400)


@app.delete("/delete/{id}")
async def delete_by_id(id: str):
    return PlainTextResponse(todo_error, status_code=500)


@app.delete("/nodes/{id}")
async def nodes(id: str):
    return PlainTextResponse(todo_error, status_code=500)


@app.get("/sales")
async def sales(date: str):
    if is_valid_date(date):
        return PlainTextResponse(ok_error, status_code=200)
    else:
        return PlainTextResponse(validation_error, status_code=400)


@app.get("/node/{id}/statistic")
async def node_statistic(id: str, dateStart: str, dateEnd: str):
    return PlainTextResponse(todo_error, status_code=500)
