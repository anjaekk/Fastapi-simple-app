import graphql
import pytest
from aiographql.client import GraphQLRequest
from user.serializers import UserAccount
import json
from graphene.test import Client
from user.serializers import UserAccount
from main import graphql_app


async def post(payload: UserAccount):
    query = UserAccount.insert().values(title=payload.title, description=payload.description)
    graphql_client = Client(graphql_app)
    return await graphql_client.execute(query=query)