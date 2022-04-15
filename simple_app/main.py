from cgitb import handler
import graphene
import graphql
from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from starlette.datastructures import URL
from user.schema import Query, Mutation
from core.database import create_table, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio_executor import AsyncioExecutor
# router = APIRouter()
app = FastAPI()
app.on_event("startup")(create_table)

graphql_app = graphene.Schema(query=Query, mutation=Mutation)

# app.add_route("/graphql", GraphQLApp(schema=graphql_app, on_get=make_playground_handler()))

# @router.get('/graphql')
# async def graphiql(request: Request):
#     request._url = URL('/graphql')
#     return await graphql_app.handle_graphiql(request=request)

# @router.post('/graphql')
# async def graphql(request: Request, authorize: AuthJWT = Depends(), db: AsyncSession = Depends(get_session)):
#     request.state.authorize = authorize
#     request.state.db = db
#     return await graphql_app.handle_graphql(request=request)

# @app.get("/graphql")
# async def graphiql(request: Request):
#     request._url = URL("/graphql")
#     return await graphql.render_playground(request=request)

@app.post("/graphql")
async def graphql_post(request: Request, session: AsyncSession = Depends(get_session)):
    # async for session in get_session():
    #     session = session
    request.state.session = session
    g_app = GraphQLApp(schema=graphql_app)
    # g_app.on_get(make_graphiql_handler())
    return await g_app

@app.get("/")
async def health_check():
    return {
        "health_check": "OK!"
    }

