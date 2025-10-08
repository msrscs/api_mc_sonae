######################################################### 
# Faculdade: Cesar School                               #
# Curso: Segurança da Informação                        #
# Período: 2025.2                                       #
# Disciplina: Projeto 2                                 #
# Professor de Projeto 2: Marlon Silva Ferreira         #
# Professor de POO: João Victor Tinoco de Souza Abreu   #
# Projeto: Automatizar a criação de conteúdos para      #
#          comunicar projetos e respectivos resultados. #
# Descrição: API MC Sonae                               #
# Arquivo: auth.py                                      #
# Equipe:                                               #
#           Artur Torres Lima Cavalcanti                #
#           Carlos Vinicius Alves de Figueiredo         #
#           Eduardo Henrique Ferreira Fonseca Barbosa   #
#           Gabriel de Medeiros Almeida                 #
#           Mauro Sérgio Rezende da Silva               #
#           Silvio Barros Tenório                       #
# Versão: 1.0                                           #
# Data: 08/10/2025                                      #
######################################################### 

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db
import bcrypt
import random
import string

# Configuração de segurança
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # type: ignore

# Esquema de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Gerar Senha Forte
def gerar_senha_forte(tamanho=12):
    # Definindo os conjuntos de caracteres
    letras_minusculas = string.ascii_lowercase
    letras_maiusculas = string.ascii_uppercase
    numeros = string.digits
    # simbolos = string.punctuation
    # simbolos = '[!@#$%^&*(),.?":{}|<>]'
    simbolos = '[!@#$%^&*(),.?:{}|]'

    # Garantindo pelo menos um caractere de cada categoria
    senha = [
        random.choice(letras_minusculas),
        random.choice(letras_maiusculas),
        random.choice(numeros),
        random.choice(simbolos)
    ]

    # Preenchendo o restante da senha com caracteres aleatórios de todas as categorias
    todos_caracteres = letras_minusculas + letras_maiusculas + numeros + simbolos
    senha.extend(random.choice(todos_caracteres) for _ in range(tamanho - 4))

    # Embaralhando os caracteres para maior aleatoriedade
    random.shuffle(senha)

    # Convertendo a lista em string
    return ''.join(senha)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        email: str = payload.get("sub") # type: ignore
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=token_data.email) # type: ignore
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.Usuario = Depends(get_current_user)):
    if current_user.status != "Ativo": # Exemplo de verificação de status # type: ignore
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user