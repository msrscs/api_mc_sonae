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
# Arquivo: tipo_router.py                               #
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

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/tipo",
    tags=["Tipos"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas
)

@router.post("/", response_model=schemas.Tipo, status_code=status.HTTP_201_CREATED)
def create_tipo(
    tipo: schemas.TipoCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_active_user)
):
    # O ID do usuário é pego do token JWT, não do corpo da requisição
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return crud.create_tipo(db=db, tipo=tipo) # type: ignore

@router.get("/{tipo_id}", response_model=schemas.Tipo)
def read_tipo(tipo_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_tipo = crud.get_tipo(db, tipo_id=tipo_id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo não encontrado")
    return db_tipo

@router.get("/", response_model=List[schemas.Tipo])
def read_tipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    tipo = crud.get_tipos(db, skip=skip, limit=limit)
    return tipo

@router.put("/{tipo_id}", response_model=schemas.Tipo)
def update_tipo(tipo_id: int, tipo: schemas.TipoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_tipo = crud.update_tipo(db, tipo_id=tipo_id, tipo=tipo) # type: ignore
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo não encontrado")
    return db_tipo

@router.delete("/{tipo_id}", response_model=schemas.Tipo)
def delete_tipo(tipo_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_tipo = crud.delete_tipo(db, tipo_id=tipo_id)
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo não encontrado")
    return db_tipo
