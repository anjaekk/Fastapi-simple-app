import graphene
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from user.schema import Query, Mutation
from core.database import create_table, connection_dispose


app = FastAPI()
app.on_event('startup')(create_table)
app.on_event('shutdown')(connection_dispose)

graphql_app = graphene.Schema(query=Query, mutation=Mutation)

app.add_route('/graphql', GraphQLApp(schema=graphql_app, on_get=make_playground_handler()))
app.add_route('/', GraphQLApp(schema=graphql_app, on_get=make_graphiql_handler()))