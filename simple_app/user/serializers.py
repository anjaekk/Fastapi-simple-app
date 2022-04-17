import graphene
from datetime import datetime
from pydantic import EmailStr
from graphene import relay
from graphene_pydantic import PydanticInputObjectType, PydanticObjectType
from sqlmodel import Field, SQLModel
from typing import Optional


class UserAccount(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(nullable=False)
    password: str = Field(max_length=120, nullable=False)
    name: str = Field(max_length=50, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class CreateUserInput(PydanticInputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    name = graphene.String(required=True)

    class Meta:
        model = UserAccount
        exclude_fields = ('created', 'is_active')


class UserType(PydanticObjectType):

    class Meta:
        model = UserAccount
        interfaces = ( relay.Node, )
        only_fields = [
            'email',
            'password',
            'name',
            'is_active',
            'created',
        ]