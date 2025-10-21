from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Usuario, Despesa
from app.database import engine, create_db_and_tables
from app.auth import get_current_user
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "ALGUMA_CHAVE_SECRETA"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/usuario/")
def register_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    user = Usuario(username=username, hashed_password=hashed_password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"username": username}

@app.post("/login/")
def login(username: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(Usuario).where(Usuario.username == username)).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

@app.post("/despesas/")
def create_despesa(despesa: Despesa, current_user: Usuario = Depends(get_current_user)):
    despesa.user_id = current_user.id
    with Session(engine) as session:
        session.add(despesa)
        session.commit()
        session.refresh(despesa)
        return despesa

@app.get("/despesas/")
def read_despesas(current_user: Usuario = Depends(get_current_user)):
    with Session(engine) as session:
        despesas = session.exec(select(Despesa).where(Despesa.user_id == current_user.id)).all()
        return despesas
