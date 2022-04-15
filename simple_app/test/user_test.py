from graphql import graphql_sync
import graphql_relay
import pytest
import asyncio
# from asyncmock import AsyncMock

# @pytest.mark.asyncio
# async def test_health_check(graphql_client):
#     response = await graphql_client
#     assert response.status_code == 200
#     assert response.json() == {"health_check": "OK!"}


from asyncio_executor import AsyncioExecutor

import graphene
from fastapi import FastAPI
import pytest_asyncio
from starlette_graphene3 import GraphQLApp

from graphene.test import Client
from main import graphql_app
from user.serializers import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from .conftest import get_session
from aiographql.client import GraphQLRequest

async def test_create_user(graphql_client):
    query = """
        mutation {
        createUser(inputData: { 
        email: "test@test.com", 
        password: "123456",
        name: "test"
        }) {
        id
        name
        email
        isActive
        created
        }
    }
    """
    type(graphql_client) 
    result = graphql_client.execute(query)
    # result = graphql_sync(query)
    # instance = User({"email":"ee@test.com", "password":"pass", "name":"namff"})
    # session.add(instance)

    # await session.commit()
    # await session.refresh(instance)
    # test_async_session.add()
    print(result)
    print("********")

    # assert result['data']['id'] == 1
    assert  result['data']['id'] ==1