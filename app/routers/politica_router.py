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
# Arquivo: politica_router.py                           #
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
    prefix="/politica",
    tags=["Políticas"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas
)

@router.post("/", response_model=schemas.Politica, status_code=status.HTTP_201_CREATED)
def create_politica(
    politica: schemas.PoliticaCreate, 
    db: Session = Depends(get_db), 
    current_user: models.Usuario = Depends(auth.get_current_active_user)
):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    # O ID do usuário é pego do token JWT, não do corpo da requisição
    return crud.create_politica(db=db, politica=politica) # type: ignore

@router.get("/{politica_id}", response_model=schemas.Politica)
def read_politica(politica_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_politica = crud.get_politica(db, politica_id=politica_id)
    if db_politica is None:
        raise HTTPException(status_code=404, detail="Política não encontrada")
    return db_politica

@router.get("/", response_model=List[schemas.Politica])
def read_politicas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    politica = crud.get_politicas(db, skip=skip, limit=limit)
    return politica

@router.put("/{politica_id}", response_model=schemas.Politica)
def update_politica(politica_id: int, politica: schemas.PoliticaCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_politica = crud.update_politica(db, politica_id=politica_id, politica=politica)
    if db_politica is None:
        raise HTTPException(status_code=404, detail="Política não encontrada")
    return db_politica

@router.delete("/{politica_id}", response_model=schemas.Politica)
def delete_politica(politica_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_politica = crud.delete_politica(db, politica_id=politica_id)
    if db_politica is None:
        raise HTTPException(status_code=404, detail="Política não encontrada")
    return db_politica
