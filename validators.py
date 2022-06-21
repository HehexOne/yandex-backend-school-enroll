from datetime import datetime
from schema import *


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
