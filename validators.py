from datetime import datetime
from schema import *
from db.db_connection import *


def is_valid_date(mts):
    try:
        datetime.strptime(mts, '%Y-%m-%dT%H:%M:%S.%f%z')
        return True
    except ValueError:
        return False


def is_valid_price(sui: ShopUnitImport):
    if (not sui.price and sui.type == ShopUnitType.CATEGORY) or \
            (sui.type == ShopUnitType.OFFER and sui.price and (0 <= sui.price <= 9223372036854775807)):
        return True
    else:
        return False


def is_valid_shop_unit_import_request(suir: ShopUnitImportRequest):
    db = RedisUnits()
    unit_ids_set = set()
    last_size = 0
    for unit in suir.items:
        val = db.get(unit.id)
        if val and val.type != unit.type:
            return False
        if not unit.name:
            return False
        if unit.type == ShopUnitType.CATEGORY and unit.price is not None:
            return False
        if unit.parentId:
            parent = db.get(unit.parentId)
            if parent:
                if parent.type == ShopUnitType.OFFER:
                    return False
        if not is_valid_price(unit):
            return False
        unit_ids_set.add(unit.id)
        if len(unit_ids_set) == last_size:
            return False
        last_size += 1
    if not is_valid_date(suir.updateDate):
        return False
    return True
