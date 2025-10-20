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
# Arquivo: permissao_router.py                          #
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

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/permissao",
    tags=["Permissões"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas
)

@router.post("/", response_model=schemas.Permissao, status_code=status.HTTP_201_CREATED)
def create_permissao(
    permissao: schemas.PermissaoCreate, 
    db: Session = Depends(get_db), 
    current_user: models.Usuario = Depends(auth.get_current_active_user)
):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    # O ID do usuário é pego do token JWT, não do corpo da requisição
    return crud.create_permissao(db=db, permissao=permissao) # type: ignore

@router.get("/{permissao_id}", response_model=schemas.Permissao)
def read_permissao(permissao_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_permissao = crud.get_permissao(db, permissao_id=permissao_id)
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
    return db_permissao

@router.get("/", response_model=List[schemas.Permissao])
def read_permissoes(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    permissao = crud.get_permissoes(db, skip=skip, limit=limit)
    return permissao

@router.put("/{permissao_id}", response_model=schemas.Permissao)
def update_permissao(permissao_id: int, permissao: schemas.PermissaoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_permissao = crud.update_permissao(db, permissao_id=permissao_id, permissao=permissao) # type: ignore
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
    return db_permissao

@router.delete("/{permissao_id}", response_model=schemas.Permissao)
def delete_permissao(permissao_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_permissao = crud.delete_permissao(db, permissao_id=permissao_id)
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
    return db_permissao
