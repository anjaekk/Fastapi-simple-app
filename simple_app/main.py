import graphene
from fastapi import FastAPI, APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from starlette.requests import Request

from user.schema import Query, Mutation
from core.database import create_table, connection_dispose, get_session



app = FastAPI()
router = APIRouter(dependencies=[Depends(get_session)])

app.on_event('startup')(create_table)
app.on_event('shutdown')(connection_dispose)

graphql_app = graphene.Schema(query=Query, mutation=Mutation)

router.add_route('/graphql', GraphQLApp(schema=graphql_app, on_get=make_playground_handler()))
app.include_router(router)


# app.add_route('/', GraphQLApp(schema=graphql_app, on_get=make_graphiql_handler()))

# @app.post('/graphql')
# async def f(request: Request, db=Depends(get_session)):
#     request.state.db = get_session
#     return await GraphQLApp(schema=graphql_app, on_get=make_playground_handler())