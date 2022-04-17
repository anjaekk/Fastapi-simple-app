import graphql
import pytest
from aiographql.client import GraphQLRequest
from user.serializers import UserAccount
import json
from graphene.test import Client
from user.serializers import UserAccount
from main import graphql_app
from httpx import AsyncClient
from . import test_env
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from asyncio_executor import AsyncioExecutor


async def test_create_user(async_client: AsyncClient, get_session: AsyncSession):
    query = """
        mutation createUser{
            createUser(inputData: { 
                email: "sssass@test.com", 
                password: "123456",
                name: "test"
            }) {
                user{
                name
                email
            }
        }
    }
    """

    res = await async_client.post("/test",json={"query": query})
    assert res.status_code == 200
    result = res.json()
    print(result)
    print("******")
    assert result['data']['createUser']['user']['name'] == "test"


async def test_create_token(async_client: AsyncClient, test_db_session: AsyncSession):
    query = """
    mutation tokenCreate {
        createToken(  
            email: "testeamil@email.com", 
            password: "testpassword",
            ) {
            accessToken
                user {
                email
            }
        }
    }  
    """
    res = await async_client.post("/graphql",json={"query": query})
    assert res.status_code == 200
    result = res.json()
    assert result['data']['createToken']['accessToken'] ==  "aa"
    assert 'errors' not in result


@pytest.mark.anyio
async def test_user_list(graphql_client):
    query = """
        query userList {
    userList {
        name
        email
    }
    }
    """
    result = graphql_client.execute(query)
    print(result)
    print("*************")
    assert 'errors' not in result





from sqlalchemy.sql import select
@pytest.mark.asyncio
async def test_one(get_session):
    session = get_session
    user = UserAccount(name="foo", email="tt@tt.com", password="rree")
    session.add(user)
    await session.commit()
    assert len((await session.execute(select(UserAccount))).scalars().all()) == 1