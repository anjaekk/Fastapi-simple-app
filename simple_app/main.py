import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from user.schema import Query, Mutation
from core.database import create_table


app = FastAPI()
app.on_event("startup")(create_table)

schema = graphene.Schema(query=Query, mutation=Mutation)
app.mount("/graphql", GraphQLApp(schema, on_get=make_playground_handler()))

@app.get("/")
async def ping():
    return {
        "health_check": "OK!"
    }