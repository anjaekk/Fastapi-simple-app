import graphene
from graphene import relay
from sqlalchemy.sql import select
from passlib.context import CryptContext
from fastapi import Depends
from core.database import async_session, get_session
from .serializers import UserAccount, CreateUserInput, UserType
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import create_access_token


PW_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
session = async_session()

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType, description='A user instance.')
    class Arguments:
        input_data = CreateUserInput(
            description='Input data for user creation.', required=True
        )

    class Meta:
        model = UserAccount
        description = 'Create a new user.' 

    @staticmethod
    async def mutate(root, info, input_data, session: AsyncSession=None):
        if session is None:
            session = async_session()
        exist_email = (
            await session.execute(
                select(UserAccount).where(UserAccount.email == input_data['email'] and user.is_active == True)
            )
        ).scalars().first()

        if exist_email is not None:
            raise Exception('Duplicate email.')

        input_data['password'] = PW_CONTEXT.hash(input_data['password'])
        user=UserAccount(**input_data)
        session.add(user)
        await session.commit()
        return CreateUser(user=user)


class CreateToken(graphene.Mutation):
    access_token = graphene.String(description='JWT token, required to authenticate.')
    user = graphene.Field(UserType, description='A user instance.')


    class Arguments:
        email = graphene.String(required=True, description='Email of a user.')
        password = graphene.String(required=True, description='Password of a user.')

    class Meta:
        description = 'Create JWT token.'
        

    @staticmethod
    async def mutate(root, info, email, password):
        user = (
            await session.execute(
                select(UserAccount).where(UserAccount.email == email)
            )
        ).scalars().first()
        if user is None or user.is_active == False:
            raise Exception('email does not exists.')

        pw_chk = PW_CONTEXT.verify(password, user.password)
        if pw_chk == False:
            raise Exception('Wrong password.')
        
        access_token = create_access_token(user.id)
        return CreateToken(access_token=access_token, user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_token = CreateToken.Field()


class Query(graphene.ObjectType):
    user_list = graphene.List(UserType)
    
    @staticmethod
    async def resolve_user_list(root, info):
        result = await session.execute(select(UserAccount))
        return result.scalars().all()