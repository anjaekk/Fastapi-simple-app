from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from user.auth import create_access_token
import pytest


async def test_create_user(async_client: AsyncClient):
    query = """""""""
        mutation createUser{
            createUser(inputData: { 
                email: "testeamil@email.com", 
                password: "testpassword",
                name: "test"
            }) {
                user{
                name
                email
            }
        }
    }
    """
    res = await async_client.post('/graphql',json={'query': query})
    result = res.json()
    assert result['data']['createUser']['user']['name'] == 'test'


async def test_create_token(async_client: AsyncClient):
    query = """""""""
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
    res = await async_client.post('/graphql',json={'query': query})
    result = res.json()
    fake_token = create_access_token(1)
    assert result['data']['createToken']['accessToken'] == fake_token


async def test_create_token_invalid_account(async_client: AsyncClient):
    query = """""""""
    mutation tokenCreate {
        createToken(  
            email: "testeamil@email.com", 
            password: "wrongpassowrd",
            ) {
            accessToken
                user {
                email
            }
        }
    }  
    """
    res = await async_client.post('/graphql',json={'query': query})
    result = res.json()
    fake_token = create_access_token(1)
    assert result['data']['createToken'] is None
    assert result['errors'][0]['message'] == 'Wrong password.'