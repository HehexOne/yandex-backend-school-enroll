import math
from collections import deque
from db.db_connection import *
from math import floor


def update_prices(start_id):
    db = RedisUnits()
    next_unit = db.get(db.get(start_id).parentId)
    while next_unit:
        if not next_unit.parentId:
            break
        next_unit = db.get(next_unit.parentId)
        if next_unit.type == ShopUnitType.OFFER:
            continue
        child_prices = []
        for child_id in next_unit.children:
            val = db.get(child_id)
            if val.price:
                child_prices.append(val.price)
            else:
                child_prices.append(0)
        mean_price = floor(sum(child_prices) / len(child_prices))
        next_unit.price = mean_price
        db.set(next_unit.id, next_unit)


def delete_category(cat_id):
    db = RedisUnits()
    unit = db.get(cat_id)
    parent_unit = db.get(unit.parentId)
    parent_unit.children.pop(parent_unit.children.index(unit.id))
    db.set(parent_unit.id, parent_unit)
    q = deque()
    q.append(unit)
    while len(q) != 0:
        unit = q.popleft()
        for child in unit.children:
            q.append(db.get(child))
        db.delete(unit.id)


def delete_offer(off_id):
    db = RedisUnits()
    unit = db.get(off_id)
    parent_unit = db.get(unit.parentId)
    parent_unit.children.pop(parent_unit.children.index(unit.id))
    db.delete(unit.id)
    db.set(parent_unit.id, parent_unit)


def get_node(node_id):
    db = RedisUnits()
    node = db.get(node_id)
    children = []
    if node.children:
        children = [get_node(child) for child in node.children]
    node.children = children
    return node


def insert_node(node: ShopUnitImport, date):
    # TODO
    pass
