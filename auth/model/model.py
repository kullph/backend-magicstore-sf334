from typing import List
from pydantic import BaseModel

class ProductData(BaseModel):
    product_id: int
    quantity: int

class RawJSONData(BaseModel):
    data: List[ProductData]
