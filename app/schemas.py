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
# Arquivo: schemas.py                                   #
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

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime

#########################################################
# Esquemas de Política
#########################################################
class PoliticaBase(BaseModel):
    permissao: str
    descricao: str

class PoliticaCreate(PoliticaBase):
    pass

class Politica(PoliticaBase):
    politicaid: int
    
    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Tipo
#########################################################
class TipoBase(BaseModel):
    tipo: str

class TipoCreate(TipoBase):
    pass

class Tipo(TipoBase):
    tipoid: int
    # permissoes: List['Permissao']

    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Permissão
#########################################################
class PermissaoBase(BaseModel):
    tipoid: int
    politicaid: int

class PermissaoCreate(PermissaoBase):
    pass

class Permissao(PermissaoBase):
    permissaoid: int
    tipo: Tipo
    politica: Politica
    
    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Usuário
#########################################################
class UsuarioBase(BaseModel):
    email: EmailStr
    nome: str
    tipoid: int
    status: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(UsuarioBase):
    ...

class UsuarioComSenhaGerada(UsuarioBase):
    senha_gerada: str

class Usuario(UsuarioBase):
    usuarioid: int
    tipou: Tipo

    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Projeto
#########################################################
class ProjetoBase(BaseModel):
    projeto: str
    status: str

class ProjetoCreate(ProjetoBase):
    pass

class Projeto(ProjetoBase):
    projetoid: int

    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Repositório do Projeto
#########################################################
class RepositorioBase(BaseModel):
    markdown: Optional[str] = None
    tipoarquivo: str
    projetoid: int
    usuarioid: int
    datahora: datetime

class RepositorioCreate(RepositorioBase):
    pass

class Repositorio(RepositorioBase):
    repositorioid: int
    projeto: Projeto
    usuario: Usuario

    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Prompt Geral
#########################################################
class PromptGeralBase(BaseModel):
    prompt: Optional[str] = None
    usuarioid: int
    datahora: datetime

class PromptGeralCreate(PromptGeralBase):
    pass

class PromptGeral(PromptGeralBase):
    promptid: int
    usuario: Usuario
    
    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas de Prompt Usuário
#########################################################
class PromptUsuarioBase(BaseModel):
    prompt: Optional[str] = None
    usuarioid: int
    datahora: datetime

class PromptUsuarioCreate(PromptUsuarioBase):
    pass

class PromptUsuario(PromptUsuarioBase):
    promptid: int
    usuario: Usuario
    
    class Config:
        # orm_mode = True
        model_config = ConfigDict(from_attributes=True) # <-- Nova sintaxe para Pydantic V2

#########################################################
# Esquemas para Token JWT
#########################################################
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None