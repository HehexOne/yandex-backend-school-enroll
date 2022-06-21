from collections import deque
from db.db_connection import *
from math import floor


def delete_category(cat_id):
    db = RedisUnits()
    unit = db.get(cat_id)
    if unit.parentId:
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


def get_node(node_id, offers=None, with_offers=False):
    if offers is None:
        offers = list()
    db = RedisUnits()
    node = db.get(node_id)
    if node.children:
        new_child = []
        for child in node.children:
            children, child_offers = get_node(child, with_offers=True)
            if children.type == ShopUnitType.OFFER:
                offers.append(children)
            else:
                offers += child_offers
            new_child.append(children)
        children = new_child
        children_prices = [o.price for o in offers]
        node.price = floor(sum(children_prices) / len(children_prices))
    elif node.type == ShopUnitType.CATEGORY:
        children = []
    else:
        children = None
    node.children = children
    if with_offers:
        return node, offers
    else:
        return node


def insert_node(node: ShopUnitImport, date):
    db = RedisUnits()
    unit = ShopUnit(**node.dict(), date=date)
    if unit.type == ShopUnitType.CATEGORY:
        val = db.get(unit.id)
        if val:
            unit.price = val.price
    if unit.parentId:
        parent_unit = db.get(unit.parentId)
        parent_unit.children.append(unit.id)
        db.set(parent_unit.id, parent_unit)
    db.set(unit.id, unit)
    while unit.parentId:
        unit = db.get(unit.parentId)
        unit.date = date
        db.set(unit.id, unit)


