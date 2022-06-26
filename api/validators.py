from datetime import datetime
from api.schema import *


def is_valid_shop_unit_import_request(suir: ShopUnitImportRequest):
    if len(set(map(lambda x: x.id, suir.items))) != len(suir.items):
        return False
    return True
