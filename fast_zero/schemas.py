from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# TODO: Deveria fazer um UserBasic?
class UserBasic(BaseModel):
    username: str
    email: EmailStr


class UserSchema(UserBasic):
    password: str


class UserPublic(UserBasic):
    user_id: int


"""
# TODO: Analisar essa sugestao do copilot.
    class Config:
        orm_mode = True
        # Permite que o Pydantic converta modelos ORM para dicionários
        # Isso é útil quando você está usando ORMs como SQLAlchemy e deseja
        # retornar modelos Pydantic a partir de instâncias de modelo ORM.
"""


class UserDB(UserSchema):
    user_id: int


class UserPublicList(BaseModel):
    users: list[UserPublic]
