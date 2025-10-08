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
# Arquivo: main.py                                      #
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

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.routers import repositorio_router 

from . import crud, models, schemas
from .database import engine, get_db
from .routers import auth_router, usuarios_router, projetos_router, prompt_geral_router, prompt_usuario_router, repositorio_router, politica_router, tipo_router, permissao_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API MC Sonae - Projeto 2 - Grupo 2",
    description='Uma API da MC Sonae: "Automatizar a criação de conteúdos para comunicar projetos e respectivos resultados". (Com autenticação JWT)',
    version="1.0.0"
)

# Inclui os roteadores na aplicação principal
app.include_router(auth_router.router)
app.include_router(usuarios_router.router)
app.include_router(projetos_router.router)
app.include_router(repositorio_router.router)
app.include_router(prompt_geral_router.router)
app.include_router(prompt_usuario_router.router)
app.include_router(politica_router.router)
app.include_router(tipo_router.router)
app.include_router(permissao_router.router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API MC Sonae - Projeto 2 - Grupo 2!"}
