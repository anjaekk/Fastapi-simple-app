import graphene
import asyncio
from fastapi import Depends
from graphene import relay
from sqlalchemy.sql import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import async_session
from .serializers import User, UserCreateInput, UserCreateType, UserList
from core import session

session = async_session()

PW_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda: UserCreateType)
    class Arguments:
        input_data = UserCreateInput(
            description='Input data for user creation', required=True
        )

    class Meta:
        model = User
        description = 'Create a new user.' 

    @staticmethod
    async def mutate(root, info, input_data):
        # async for session in get_session():
        #     session = session

        exist_email = (
            await session.execute(
                select(User).where(User.email == input_data['email'])
            )
        ).scalars().first()

        if exist_email is not None:
            raise Exception("Email already exists.")

        input_data['password'] = PW_CONTEXT.hash(input_data['password'])
        # instance = User(**input_data)
        user=User()
        user.email = input_data["email"]
        user.password = input_data["password"]
        user.name = input_data["name"] 
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(user)
        print("***************")
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user_list = graphene.List(UserList)

    @staticmethod
    def resolve_user_list(root, info):
        return select(UserList).all()