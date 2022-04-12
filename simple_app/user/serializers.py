from datetime import datetime
from pydantic import EmailStr
from graphene import relay
from graphene_pydantic import PydanticInputObjectType, PydanticObjectType
from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    email: EmailStr = Field(nullable=False)
    password: str = Field(max_length=120, nullable=False)
    name: str = Field(max_length=50, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created: datetime = Field(default_factory=datetime.now)
    jwt_token_key: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreateInput(PydanticInputObjectType):
    class Meta:
        model = User
        exclude_fields = ('id', 'created', 'is_active')


class UserCreate(PydanticObjectType):
    class Meta:
        model = User
        interfaces = ( relay.Node, )


class UserList(PydanticObjectType):
    class Meta:
        model = User