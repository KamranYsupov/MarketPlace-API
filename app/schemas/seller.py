import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import Field

from .mixins import SellerSchemaMixin

from .product import ProductSchema


class SellerSchema(SellerSchemaMixin):
    id: uuid.UUID
                   

class SellerProductsSchema(SellerSchema):
    products: list[ProductSchema]
    
                       
class CreateSellerSchema(SellerSchemaMixin):
    user_id: Optional[uuid.UUID] = Field(default=None)