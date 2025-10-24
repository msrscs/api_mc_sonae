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
# Arquivo: projetos_router.py                           #
# Equipe:                                               #
#           Artur Torres Lima Cavalcanti                #
#           Carlos Vinicius Alves de Figueiredo         #
#           Eduardo Henrique Ferreira Fonseca Barbosa   #
#           Gabriel de Medeiros Almeida                 #
#           Mauro Sérgio Rezende da Silva               #
#           Silvio Barros Tenório                       #
# Versão: 1.0                                           #
# Data: 24/10/2025                                      #
######################################################### 

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/projetos",
    tags=["Projetos"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas
)

@router.post("/", response_model=schemas.Projeto, status_code=status.HTTP_201_CREATED)
def create_projeto(projeto: schemas.ProjetoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return crud.create_projeto(db=db, projeto=projeto)

@router.get("/", response_model=List[schemas.Projeto])
def read_projetos(skip: int = 0, limit: int = 1000, filtro: str = "", db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    projetos = crud.get_projetos(db, skip=skip, limit=limit)
    return projetos

@router.get("/{projeto_id}", response_model=schemas.Projeto)
def read_projeto(projeto_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_projeto = crud.get_projeto(db, projeto_id=projeto_id)
    if db_projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return db_projeto

@router.put("/{projeto_id}", response_model=schemas.Projeto)
def update_projeto(projeto_id: int, projeto: schemas.ProjetoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_projeto = crud.update_projeto(db, projeto_id=projeto_id, projeto=projeto)
    if db_projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return db_projeto

@router.delete("/{projeto_id}", response_model=schemas.Projeto)
def delete_projeto(projeto_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_projeto = crud.delete_projeto(db, projeto_id=projeto_id)
    if db_projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return db_projeto