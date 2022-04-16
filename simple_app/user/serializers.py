import graphene
from datetime import datetime
from pydantic import EmailStr
from graphene import relay
from graphene_pydantic import PydanticInputObjectType, PydanticObjectType
from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(nullable=False)
    password: str = Field(max_length=120, nullable=False)
    name: str = Field(max_length=50, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created: datetime = Field(default_factory=datetime.now)
    jwt_token_key: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreateInput(PydanticInputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    name = graphene.String(required=True)
    jwt_token_key = graphene.String(required=False)
    class Meta:
        model = User
        exclude_fields = ('created', 'is_active')


class UserCreateType(PydanticObjectType):
    name = graphene.String()
    password = graphene.String(required=True)
    name = graphene.String(required=True)
    jwt_token_key = graphene.String(required=False)
    class Meta:
        model = User
        interfaces = ( relay.Node, )


class UserList(PydanticObjectType):
    class Meta:
        model = User