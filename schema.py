from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


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
    children: List = []


class ShopUnitImport(BaseModel):
    id: str
    name: str
    parentId: Optional[str] = None
    type: ShopUnitType
    price: Optional[int] = None


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: str


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
