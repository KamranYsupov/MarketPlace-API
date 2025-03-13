from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base, AbstractUser, TimestampedMixin


if TYPE_CHECKING:
    from .seller import Seller


class User(AbstractUser, TimestampedMixin):
    """Модель пользователя"""

    bill: Mapped[float] = mapped_column(default=0)

    cart: Mapped[list['CartItem']] = relationship(
        lazy='selectin',
        cascade='all, delete',
    )
    favorites: Mapped[list['Product']] = relationship(
        secondary='user_favorite_products',
        lazy='selectin',
        cascade='all, delete',
    )

    seller: Mapped['Seller'] = relationship(back_populates='user')


class UserFavoriteProductsAssociation(Base):
    """Модель для ManyToMany поля User.favorites"""
    __tablename__ = 'user_favorite_products'

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE')
    )


class CartItem(Base):
    """Модель элемента корзины"""

    quantity: Mapped[int] = mapped_column(default=1)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
    )


