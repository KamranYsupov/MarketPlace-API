from typing import Dict, Any

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.db import User, Seller
from app.db.transaction import atomic
from app.schemas.product import CreateProductSchema, ProductSchema
from app.schemas.seller import SellerSchema
from app.services import ProductService, SellerService
from ..deps import get_current_user_access, get_current_seller

router = APIRouter(tags=['Product'], prefix='/products')


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductSchema,
)
@inject
async def create_product(
    create_product_schema: CreateProductSchema,
    seller: Seller = Depends(get_current_seller),
    product_service: ProductService = Depends(Provide[Container.product_service]),
) -> ProductSchema:
    create_product_schema.seller_id = seller.id
    product = await product_service.create(obj_in=create_product_schema)
    product_schema = ProductSchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        rating=product.rating,
        quantity=product.quantity,
    )
    return product_schema