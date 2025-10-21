from sqlmodel import SQLModel, Field
from typing import Optional

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

class Despesa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    descricao: str
    valor: float
    categoria: str
