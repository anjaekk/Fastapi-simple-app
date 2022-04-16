import graphene
from graphene import relay
from sqlalchemy.sql import select
from passlib.context import CryptContext

from core.database import async_session
from .serializers import User, UserCreateInput, UserCreateType, UserList


PW_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
session = async_session()

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

        exist_email = (
            await session.execute(
                select(User).where(User.email == input_data['email'])
            )
        ).scalars().first()

        if exist_email is not None:
            raise Exception("Email already exists.")

        input_data['password'] = PW_CONTEXT.hash(input_data['password'])
        user=User(**input_data)
        session.add(user)
        await session.commit()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user_list = graphene.List(UserList)

    @staticmethod
    async def resolve_user_list(root, info):
        result = await session.execute(select(UserList).all())
        return result