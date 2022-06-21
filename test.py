import json

from db.db_connection import *
from db.db_utils import *
from pprint import pprint

db = RedisUnits()

db.set("3fa85f64-5717-4562-b3fc-2c963f66a333", ShopUnit(**{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
    "name": "Object1",
    "parentId": None,
    "date": "2022-05-28T21:12:01.000Z",
    "price": 277,
    "type": "CATEGORY",
    "children": ['3fa85f64-5717-4562-b3fc-2c963f66a222', '3fa85f64-5717-4562-b3fc-2c963f66a444']
}))

db.set("3fa85f64-5717-4562-b3fc-2c963f66a444", ShopUnit(**{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
    "name": "Object2",
    "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333",
    "date": "2022-05-28T21:12:02.000Z",
    "price": None,
    "type": "CATEGORY",
    "children": []
}))

db.set("3fa85f64-5717-4562-b3fc-2c963f66a222", ShopUnit(**{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
    "name": "Object3",
    "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333",
    "date": "2022-05-28T21:12:03.000Z",
    "price": 234,
    "type": "CATEGORY",
    "children": ['3fa85f64-5717-4562-b3fc-2c963f66a111']
}))

db.set("3fa85f64-5717-4562-b3fc-2c963f66a111", ShopUnit(**{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
    "name": "Object4",
    "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a222",
    "date": "2022-05-28T21:12:04.000Z",
    "price": 234,
    "type": "OFFER",
    "children": []
}))

# print(ShopUnit(**db.get("3fa85f64-5717-4562-b3fc-2c963f66a111")))

update_prices("3fa85f64-5717-4562-b3fc-2c963f66a111")

print(get_node("3fa85f64-5717-4562-b3fc-2c963f66a333").json())
