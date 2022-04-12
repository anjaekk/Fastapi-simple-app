import graphene
from graphene import relay

from core.database import async_session
from .serializers import User, UserCreateInput, UserCreate, UserList
from .models import User as user_model


class CreateUser(graphene.Mutation):
    class Arguments:
        input_data = UserCreateInput(
            description="Input data for user creation", required=True
        )

    class Meta:
        model = user_model
        description = "Create a new user."
        
    Output = UserCreate

    @staticmethod
    async def mutate(self, info, input_data):
        instance = User(**input_data)
        session = async_session()

        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user_list = graphene.List(UserList)

    @staticmethod
    def resolve_user_list(root, info):
        return UserList.all()