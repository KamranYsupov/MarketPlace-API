import strawberry
from strawberry.fastapi import GraphQLRouter
from dependency_injector.wiring import Provide, inject

from .queries.base import BaseQuery
from .context import get_context

@strawberry.type
class Query(BaseQuery):
    pass


schema = strawberry.Schema(Query)

router = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=True,
)