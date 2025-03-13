import uuid
from typing import TYPE_CHECKING, Optional, ForwardRef

from pydantic import BaseModel, Field

from .mixins import ProductSchemaMixin


class ProductSchema(ProductSchemaMixin):
    id: uuid.UUID


class CreateProductSchema(ProductSchemaMixin):
    seller_id: Optional[uuid.UUID] = Field(title='ID продавца', default=None)
  


    