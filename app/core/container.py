from dependency_injector import containers, providers

from app.repositories import (
    RepositoryUser,
    RepositoryRefreshToken,
    RepositoryProduct, 
    RepositorySeller,
    RepositoryOrder,
    RepositoryOrderItem,
)
from app.services import (
    UserService,
    JWTService,
    ProductService,
    SellerService,
    OrderService,
)
from app.db import (
    DataBaseManager,
    User,
    RefreshToken,
    Product,
    Seller,
    Order,
    OrderItem,
)
from app.core.config import settings




class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_user = providers.Singleton(
        RepositoryUser, model=User, session=session
    )
    repository_product = providers.Singleton(
        RepositoryProduct, model=Product, session=session
    )
    repository_seller = providers.Singleton(
        RepositorySeller, model=Seller, session=session
    )
    repository_refresh_token = providers.Singleton(
        RepositoryRefreshToken, model=RefreshToken, session=session
    )
    repository_order = providers.Singleton(
        RepositoryOrder, model=Order, session=session
    )
    repository_order_item = providers.Singleton(
        RepositoryOrderItem, model=OrderItem, session=session
    )
    # endregion

    # region services
    user_service = providers.Singleton(
        UserService, 
        repository_user=repository_user, 
        unique_fields=('username', 'email')
    )
    product_service = providers.Singleton(
        ProductService,
        repository_product=repository_product,
    )
    order_service = providers.Singleton(
        OrderService,
        repository_product=repository_product,
        repository_order=repository_order,
        repository_order_item=repository_order_item,
    )
    seller_service = providers.Singleton(
        SellerService, 
        repository_seller=repository_seller,
        unique_fields=('name', 'user_id'),
    )
    jwt_service = providers.Singleton(
        JWTService, repository_refresh_token=repository_refresh_token
    )
    # endregion


container = Container()
container.init_resources()
container.wire(modules=settings.container_wiring_modules)
