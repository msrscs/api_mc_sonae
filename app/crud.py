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
# Arquivo: crud.py                                      #
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
from httpx import get
from sqlalchemy.orm import Session, selectinload
from . import models, schemas, auth

#########################################################
# --- CRUD Usuários ---
#########################################################
def get_user(db: Session, user_id: int):
    return db.query(models.Usuario).options(selectinload(models.Usuario.tipou)).filter(models.Usuario.usuarioid == user_id).first()  # type: ignore

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).options(selectinload(models.Usuario.tipou)).filter(models.Usuario.email == email).first()  # type: ignore

def get_users(db: Session, skip: int = 0, limit: int = 1000, filtro: str = ""):
    if filtro:
        return db.query(models.Usuario).options(selectinload(models.Usuario.tipou)).filter(models.Usuario.nome.ilike(f"%{filtro}%")).order_by(models.Usuario.nome).offset(skip).limit(limit).all() # type: ignore
    return db.query(models.Usuario).options(selectinload(models.Usuario.tipou)).order_by(models.Usuario.nome).offset(skip).limit(limit).all() # type: ignore

def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = auth.get_password_hash(user.senha)
    db_user = models.Usuario(
        email=user.email, 
        senha=hashed_password, 
        nome=user.nome,
        tipoid=user.tipoid,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UsuarioCreate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.nome = user.nome # type: ignore
        db_user.tipoid = user.tipoid # type: ignore
        db_user.status = user.status # type: ignore
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def change_password_user(db: Session, user_id: int, user: schemas.UsuarioCreate):
    db_user = get_user(db, user_id)
    if db_user:
       hashed_password = auth.get_password_hash(user.senha)
       db_user.senha=hashed_password # type: ignore
    db.commit()
    db.refresh(db_user)
    return db_user

def reset_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
       gsenha=auth.gerar_senha_forte(12)
       hashed_password = auth.get_password_hash(gsenha)
       db_user.senha=hashed_password  # type: ignore
    db.commit()
    db.refresh(db_user)
    return db_user, gsenha

def verifica_user(db: Session, modulo_permissao: List[str], current_user):
    print (f"####################################################################")
    print (f"Verificando permissões para o usuário: {current_user.email} {current_user.usuarioid}")
    user_tipoid = current_user.tipoid  # type: ignore
    print (f"Tipo ID do usuário atual: {user_tipoid}")
    db_permissao = db.query(models.Permissao).options(selectinload(models.Permissao.politica), selectinload(models.Permissao.tipo)).filter(models.Permissao._tipoid == user_tipoid).all()
    print (f"Permissões do usuário: {[permissao.politica.permissao for permissao in db_permissao]}")
    print (f"####################################################################")
    for permissao in db_permissao:  
        if permissao.politica.permissao in modulo_permissao:
             return True
    return False

#########################################################
# --- CRUD Projetos ---
#########################################################
def get_projeto(db: Session, projeto_id: int):
    return db.query(models.Projeto).filter(models.Projeto.projetoid == projeto_id).first() # type: ignore

def get_projetos(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Projeto).order_by(models.Projeto.projeto).offset(skip).limit(limit).all() # type: ignore

def create_projeto(db: Session, projeto: schemas.ProjetoCreate):
    db_projeto = models.Projeto(**projeto.dict())
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto

def update_projeto(db: Session, projeto_id: int, projeto: schemas.ProjetoCreate):
    db_projeto = get_projeto(db, projeto_id)
    if db_projeto:
        db_projeto.projeto = projeto.projeto # type: ignore
        db_projeto.status = projeto.status # type: ignore
        db.commit()
        db.refresh(db_projeto)
    return db_projeto

def delete_projeto(db: Session, projeto_id: int):
    db_projeto = get_projeto(db, projeto_id)
    if db_projeto:
        db.delete(db_projeto)
        db.commit()
    return db_projeto

#########################################################
# --- CRUD Repositório ---
#########################################################
def get_repositorio(db: Session, repositorio_id: int):
    return db.query(models.Repositorio).options(selectinload(models.Repositorio.projeto), selectinload(models.Repositorio.usuario)).filter(models.Repositorio.repositorioid == repositorio_id).first() # type: ignore


def get_repositorios(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Repositorio).options(selectinload(models.Repositorio.projeto), selectinload(models.Repositorio.usuario)).order_by(models.Repositorio.datahora.desc()).offset(skip).limit(limit).all() # type: ignore

def create_repositorio(db: Session, repositorio: schemas.RepositorioCreate, user_id: int):
    data = repositorio.dict()
    data["usuarioid"] = user_id
    db_repositorio = models.Repositorio(**data)
    db.add(db_repositorio)
    db.commit()
    db.refresh(db_repositorio)
    return db_repositorio

def update_repositorio(db: Session, repositorio_id: int, repositorio: schemas.RepositorioCreate, user_id: int):
    db_repositorio = get_repositorio(db, repositorio_id)
    if db_repositorio:
        db_repositorio.projetoid = repositorio.projetoid # type: ignore
        db_repositorio.usuarioid = user_id # type: ignore
        db_repositorio.tipoarquivo = repositorio.tipoarquivo # type: ignore
        db_repositorio.markdown = repositorio.markdown # type: ignore
        db_repositorio.datahora = repositorio.datahora # type: ignore
        db.commit()
        db.refresh(db_repositorio)
    return db_repositorio

def delete_repositorio(db: Session, repositorio_id: int):
    # db_repositorio = db.query(models.Repositorio).options(selectinload(models.Repositorio.projeto), selectinload(models.Repositorio.usuario)).filter(models.Repositorio.repositorioid == repositorio_id).first()
    db_repositorio = get_repositorio(db, repositorio_id)
    if db_repositorio:
        db.delete(db_repositorio)
        db.commit()
    return db_repositorio

#########################################################
# --- CRUD Prompt Geral ---
#########################################################
def get_prompt_geral(db: Session, prompt_id: int):
    return db.query(models.PromptGeral).options(selectinload(models.PromptGeral.usuario)).filter(models.PromptGeral.promptid == prompt_id).first() # type: ignore

def get_prompts_geral(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.PromptGeral).options(selectinload(models.PromptGeral.usuario)).order_by(models.PromptGeral.datahora.desc()).offset(skip).limit(limit).all() # type: ignore

def create_prompt_geral(db: Session, prompt: schemas.PromptGeralCreate, user_id: int):
    data = prompt.dict()
    data["usuarioid"] = user_id
    db_prompt = models.PromptGeral(**data)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def update_prompt_geral(db: Session, prompt_id: int, prompt: schemas.PromptGeralCreate, user_id: int):
    db_prompt_geral = get_prompt_geral(db, prompt_id)
    if db_prompt_geral:
        db_prompt_geral.prompt = prompt.prompt # type: ignore
        db_prompt_geral.usuarioid = user_id # type: ignore
        db_prompt_geral.datahora = prompt.datahora # type: ignore
        db.commit()
        db.refresh(db_prompt_geral)
    return db_prompt_geral

def delete_prompt_geral(db: Session, prompt_id: int):
    db_prompt_geral = get_prompt_geral(db, prompt_id)
    if db_prompt_geral:
        db.delete(db_prompt_geral)
        db.commit()
    return db_prompt_geral

#########################################################
# --- CRUD Prompt Usuário ---
#########################################################
def get_prompt_usuario(db: Session, prompt_id: int):
    return db.query(models.PromptUsuario).options(selectinload(models.PromptUsuario.usuario)).filter(models.PromptUsuario.promptid == prompt_id).first() # type: ignore

def get_prompts_usuario(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.PromptUsuario).options(selectinload(models.PromptUsuario.usuario)).order_by(models.PromptUsuario.datahora.desc()).offset(skip).limit(limit).all() # type: ignore

def create_prompt_usuario(db: Session, prompt: schemas.PromptUsuarioCreate, user_id: int):
    data = prompt.dict()
    data["usuarioid"] = user_id
    db_prompt = models.PromptUsuario(**data)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def update_prompt_usuario(db: Session, prompt_id: int, prompt: schemas.PromptUsuarioCreate, user_id: int):
    db_prompt_usuario = get_prompt_usuario(db, prompt_id)
    if db_prompt_usuario:
        db_prompt_usuario.prompt = prompt.prompt # type: ignore
        db_prompt_usuario.usuarioid = user_id # type: ignore
        db_prompt_usuario.datahora = prompt.datahora # type: ignore
        db.commit()
        db.refresh(db_prompt_usuario)
    return db_prompt_usuario

def delete_prompt_usuario(db: Session, prompt_id: int):
    db_prompt_usuario = get_prompt_usuario(db, prompt_id)
    if db_prompt_usuario:
        db.delete(db_prompt_usuario)
        db.commit()
    return db_prompt_usuario

#########################################################
# --- CRUD Politica ---
#########################################################
def get_politica(db: Session, politica_id: int):
    return db.query(models.Politica).filter(models.Politica.politicaid == politica_id).first() # type: ignore

def get_politicas(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Politica).order_by(models.Politica.permissao).offset(skip).limit(limit).all() # type: ignore

def create_politica(db: Session, politica: schemas.PoliticaCreate):
    db_politica = models.Politica(**politica.dict())
    db.add(db_politica)
    db.commit()
    db.refresh(db_politica)
    return db_politica

def update_politica(db: Session, politica_id: int, politica: schemas.PoliticaCreate):
    db_politica = get_politica(db, politica_id)
    if db_politica:
        db_politica.permissao = politica.permissao # type: ignore
        db_politica.descricao = politica.descricao # type: ignore
        db.commit()
        db.refresh(db_politica)
    return db_politica

def delete_politica(db: Session, politica_id: int):
    db_politica = get_politica(db, politica_id)
    if db_politica:
        db.delete(db_politica)
        db.commit()
    return db_politica

#########################################################
# --- CRUD Tipo ---
#########################################################
def get_tipo(db: Session, tipo_id: int):
    return db.query(models.Tipo).options(selectinload(models.Tipo.permissoes)).filter(models.Tipo.tipoid == tipo_id).first() # type: ignore

def get_tipos(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Tipo).options(selectinload(models.Tipo.permissoes)).order_by(models.Tipo.tipo).offset(skip).limit(limit).all() # type: ignore

def create_tipo(db: Session, tipo: schemas.TipoCreate):
    db_tipo = models.Tipo(**tipo.dict())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

def update_tipo(db: Session, tipo_id: int, tipo: schemas.TipoCreate):
    db_tipo = get_tipo(db, tipo_id)
    if db_tipo:
        db_tipo.tipo = tipo.tipo # type: ignore
        db.commit()
        db.refresh(db_tipo)
    return db_tipo

def delete_tipo(db: Session, tipo_id: int):
    db_tipo = get_tipo(db, tipo_id)
    if db_tipo:
        db.delete(db_tipo)
        db.commit()
    return db_tipo

#########################################################
# --- CRUD Permissão ---
#########################################################
def get_permissao(db: Session, permissao_id: int):
    return db.query(models.Permissao).options(selectinload(models.Permissao.politica), selectinload(models.Permissao.tipo)).filter(models.Permissao.permissaoid == permissao_id).first() # type: ignore

def get_permissoes(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Permissao).options(selectinload(models.Permissao.politica), selectinload(models.Permissao.tipo)).order_by(models.Permissao.tipoid).offset(skip).limit(limit).all() # type: ignore

def create_permissao(db: Session, permissao: schemas.PermissaoCreate):
    db_permissao = models.Permissao(**permissao.dict())
    db.add(db_permissao)
    db.commit()
    db.refresh(db_permissao)
    return db_permissao

def update_permissao(db: Session, permissao_id: int, permissao: schemas.PermissaoCreate):
    db_permissao = get_permissao(db, permissao_id)
    if db_permissao:
        db_permissao.tipoid = permissao.tipoid # type: ignore
        db_permissao.politicaid = permissao.politicaid # type: ignore
        db.commit()
        db.refresh(db_permissao)
    return db_permissao

def delete_permissao(db: Session, permissao_id: int):
    db_permissao = get_permissao(db, permissao_id)
    if db_permissao:
        db.delete(db_permissao)
        db.commit()
    return db_permissao
