from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


# TODO: Deveria fazer um UserBasic?
class UserBasic(BaseModel):
    username: str
    email: EmailStr


class UserSchema(UserBasic):
    password: str


class UserPublic(UserBasic):
    id: int
    model_config = ConfigDict(from_attributes=True)


""" # * tem o mesmo efeito do ConfigDict(from_attributes=True)
    class Config: # tem o mesmo efeito do from_attributes=True
        orm_mode = True
        # Permite que o Pydantic converta modelos ORM para dicionários
        # Isso é útil quando você está usando ORMs como SQLAlchemy e deseja
        # retornar modelos Pydantic a partir de instâncias de modelo ORM.
"""


class UserPublicList(BaseModel):
    users: list[UserPublic]
