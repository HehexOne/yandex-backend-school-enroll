import json

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(json.dumps({
        "code": 400,
        "message": "Validation Failed"
    }), status_code=400)


@app.post("/imports")
def imports():
    return {"message": "TODO"}


@app.delete("/delete/{id}")
def delete_by_id(id: int):
    return {"message": "TODO"}


@app.delete("/nodes/{id}")
def nodes(id: int):
    return {"message": "TODO"}


@app.get("/sales")
def sales():
    return {"message": "TODO"}


@app.get("/node/{id}/statistic")
def node_statistic(id: int):
    return {"message": "TODO"}
