import graphene
from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from user.schema import Query, Mutation
from core.database import create_table


# router = APIRouter()
app = FastAPI()
app.on_event("startup")(create_table)

graphql_app = graphene.Schema(query=Query, mutation=Mutation)

app.add_route("/graphql", GraphQLApp(schema=graphql_app, on_get=make_playground_handler()))


@app.get("/")
async def health_check():
    return {
        "health_check": "OK!"
    }