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
# Arquivo: usuarios_router.py                           #
# Equipe:                                               #
#           Artur Torres Lima Cavalcanti                #
#           Carlos Vinicius Alves de Figueiredo         #
#           Eduardo Henrique Ferreira Fonseca Barbosa   #
#           Gabriel de Medeiros Almeida                 #
#           Mauro Sérgio Rezende da Silva               #
#           Silvio Barros Tenório                       #
# Versão: 1.0                                           #
# Data: 26/10/2025                                      #
######################################################### 

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas deste router
)

@router.post("/", response_model=schemas.Usuario, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
     if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
     db_user = crud.get_user_by_email(db, email=user.email)
     if db_user:
         raise HTTPException(status_code=400, detail="E-mail já cadastrado")
     return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.Usuario])
def read_users(skip: int = 0, limit: int = 1000, filtro: str = "", db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    users = crud.get_users(db, skip=skip, limit=limit, filtro=filtro)
    return users

@router.get("/me", response_model=schemas.Usuario)
async def read_users_me(db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA","PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user

@router.get("/{user_id}", response_model=schemas.Usuario)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.put("/{user_id}", response_model=schemas.Usuario)
def update_user(user_id: int, user: schemas.UsuarioUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_user = crud.update_user(db, user_id=user_id, user=user) # type: ignore
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.delete("/{user_id}", response_model=schemas.Usuario)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.put("/change_password/{user_id}", response_model=schemas.Usuario)
def change_password_user(user_id: int, user: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN","USR:ESCRITA","USR:LEITURA","PRJ:ADMIN","PRJ:ESCRITA","PRJ:LEITURA"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_user = crud.change_password_user(db, user_id=current_user.usuarioid, user=user) # type: ignore
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.put("/reset/{user_id}", response_model=schemas.UsuarioComSenhaGerada)
def reset_user(user_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_active_user)):
    if not crud.verifica_user(db, ["USR:ADMIN"], current_user):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_user, gsenha = crud.reset_user(db, user_id=user_id) # type: ignore
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    response_data = {
        "usuarioid": db_user.usuarioid,
        "email": db_user.email,
        "nome": db_user.nome,
        "tipoid": db_user.tipoid,
        "status": db_user.status,
        "senha_gerada": gsenha
    }
    # print("Senha Gerada: ", gsenha)
    return response_data
