from datetime import datetime, timezone
from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional, List


def is_valid_date(mts) -> (bool, datetime):
    try:
        v = datetime.strptime(mts, '%Y-%m-%dT%H:%M:%S.%f%z')
        return True, v
    except ValueError:
        return False, None


class ShopUnitType(str, Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopUnit(BaseModel):
    id: str
    name: str
    date: str
    parentId: Optional[str] = None
    type: ShopUnitType
    price: Optional[int] = None
    children: Optional[List]

    @validator('date')
    def date_valid(cls, v):
        res, val = is_valid_date(v)
        if not res:
            raise ValueError("Failed to validate")
        return datetime.timestamp(val)


class ShopUnitImport(BaseModel):
    id: str
    name: str
    parentId: Optional[str] = None
    type: ShopUnitType
    price: Optional[int] = None


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: str

    @validator('updateDate')
    def date_valid(cls, v):
        res, val = is_valid_date(v)
        if not res:
            raise ValueError("Failed to validate")
        return datetime.timestamp(val)


class ShopUnitStatisticUnit(BaseModel):
    id: str
    name: str
    parentId: Optional[str] = None
    type: ShopUnitType
    price: Optional[int] = None
    date: str


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit] = []


class Error(BaseModel):
    code: int
    message: str
