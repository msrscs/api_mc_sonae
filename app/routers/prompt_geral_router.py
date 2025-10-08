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
# Arquivo: prompt_geral_router.py                       #
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
    prefix="/promptgeral",
    tags=["Prompt Geral"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas
)

@router.post("/", response_model=schemas.PromptGeral, status_code=status.HTTP_201_CREATED)
def create_prompt_geral(
    prompt: schemas.PromptGeralCreate, 
    db: Session = Depends(get_db), 
    current_user: models.Usuario = Depends(auth.get_current_active_user)
):
    if not crud.verifica_user(db, ["PRJ:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    # O ID do usuário é pego do token JWT, não do corpo da requisição
    return crud.create_prompt_geral(db=db, prompt=prompt, user_id=current_user.usuarioid) # type: ignore

@router.get("/{prompt_id}", response_model=schemas.PromptGeral)
def read_prompt_geral(prompt_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_prompt_geral = crud.get_prompt_geral(db, prompt_id=prompt_id)
    if db_prompt_geral is None:
        raise HTTPException(status_code=404, detail="Prompt Geral não encontrado")
    return db_prompt_geral

@router.get("/", response_model=List[schemas.PromptGeral])
def read_prompts_geral(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    prompt = crud.get_prompts_geral(db, skip=skip, limit=limit)
    return prompt

@router.put("/{prompt_id}", response_model=schemas.PromptGeral)
def update_prompt_geral(prompt_id: int, prompt: schemas.PromptGeralCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_prompt_geral = crud.update_prompt_geral(db, prompt_id=prompt_id, prompt=prompt, user_id=current_user.usuarioid) # type: ignore
    if db_prompt_geral is None:
        raise HTTPException(status_code=404, detail="Prompt Geral não encontrado")
    return db_prompt_geral

@router.delete("/{prompt_id}", response_model=schemas.PromptGeral)
def delete_prompt_geral(prompt_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["PRJ:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_prompt_geral = crud.delete_prompt_geral(db, prompt_id=prompt_id)
    if db_prompt_geral is None:
        raise HTTPException(status_code=404, detail="Prompt Geral não encontrado")
    return db_prompt_geral