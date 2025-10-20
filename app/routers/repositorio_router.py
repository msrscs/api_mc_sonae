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
# Arquivo: repositorio_router.py                        #
# Equipe:                                               #
#           Artur Torres Lima Cavalcanti                #
#           Carlos Vinicius Alves de Figueiredo         #
#           Eduardo Henrique Ferreira Fonseca Barbosa   #
#           Gabriel de Medeiros Almeida                 #
#           Mauro Sérgio Rezende da Silva               #
#           Silvio Barros Tenório                       #
# Versão: 1.0                                           #
# Data: 20/10/2025                                      #
######################################################### 

import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/repositorio",
    tags=["Repositório dos Projetos"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas
)

@router.post("/", response_model=schemas.Repositorio, status_code=status.HTTP_201_CREATED)
def create_repositorio(repositorio: schemas.RepositorioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return crud.create_repositorio(db=db, repositorio=repositorio, user_id=current_user.usuarioid) # type: ignore

@router.get("/", response_model=List[schemas.Repositorio])
def read_repositorios(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    repositorio = crud.get_repositorios(db, skip=skip, limit=limit)
    return repositorio

@router.get("/{repositorio_id}", response_model=schemas.Repositorio)
def read_repositorio(repositorio_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_repositorio = crud.get_repositorio(db, repositorio_id=repositorio_id)
    if db_repositorio is None:
        raise HTTPException(status_code=404, detail="Repositório não encontrado")
    return db_repositorio

@router.put("/{repositorio_id}", response_model=schemas.Repositorio)
def update_repositorio(repositorio_id: int, repositorio: schemas.RepositorioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_repositorio = crud.update_repositorio(db, repositorio_id=repositorio_id, repositorio=repositorio, user_id=current_user.usuarioid) # type: ignore
    if db_repositorio is None:
        raise HTTPException(status_code=404, detail="Repositório não encontrado")
    return db_repositorio

@router.delete("/{repositorio_id}", response_model=schemas.Repositorio)
def delete_repositorio(repositorio_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_repositorio = crud.delete_repositorio(db, repositorio_id=repositorio_id)
    if db_repositorio is None:
        raise HTTPException(status_code=404, detail="Repositório não encontrado")
    return db_repositorio