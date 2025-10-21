from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Despesa(BaseModel):
    id: int
    descricao: str
    valor: float
    categoria: str

# Dados simulados
despesas = []

@router.get("/", response_model=List[Despesa])
def listar_despesas():
    return despesas

@router.post("/", response_model=Despesa)
def criar_despesa(despesa: Despesa):
    despesas.append(despesa)
    return despesa

@router.delete("/{id}")
def remover_despesa(id: int):
    global despesas
    despesas = [d for d in despesas if d.id != id]
    return {"mensagem": "Despesa removida com sucesso!"}