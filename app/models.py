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
# Arquivo: models.py                                    #
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

import re
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Usuario(Base):
    __tablename__ = 'tb_usuarios'
    __table_args__ = {'schema': 'p2'}

    usuarioid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    nome = Column(String(50), nullable=False)
    tipoid = Column(Integer, ForeignKey('p2.tb_tipos.tipoid'), nullable=False)
    status = Column(String(15), nullable=False)

    # Relacionamentos
    promptgeral = relationship("PromptGeral", back_populates="usuario")
    promptusuario = relationship("PromptUsuario", back_populates="usuario")
    repositorios = relationship("Repositorio", back_populates="usuario")
    tipou = relationship("Tipo", back_populates="usuario")

class Projeto(Base):
    __tablename__ = 'tb_projetos'
    __table_args__ = {'schema': 'p2'}

    projetoid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    projeto = Column(String(100), nullable=False)
    status = Column(String(15), nullable=False)
    
    # Relacionamentos
    repositorios = relationship("Repositorio", back_populates="projeto")

class Repositorio(Base):
    __tablename__ = 'tb_repositorio_pj'
    __table_args__ = {'schema': 'p2'}

    repositorioid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    projetoid = Column(Integer, ForeignKey('p2.tb_projetos.projetoid'), nullable=False)
    usuarioid = Column(Integer, ForeignKey('p2.tb_usuarios.usuarioid'), nullable=False)
    markdown = Column(Text)
    datahora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    projeto = relationship("Projeto", back_populates="repositorios")
    usuario = relationship("Usuario", back_populates="repositorios")

class PromptGeral(Base):
    __tablename__ = 'tb_prompt_geral'
    __table_args__ = {'schema': 'p2'}
    
    promptid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    prompt = Column(Text)
    usuarioid = Column(Integer, ForeignKey('p2.tb_usuarios.usuarioid'), nullable=False)
    datahora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="promptgeral")

class PromptUsuario(Base):
    __tablename__ = 'tb_prompt_usuario'
    __table_args__ = {'schema': 'p2'}
    
    promptid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    usuarioid = Column(Integer, ForeignKey('p2.tb_usuarios.usuarioid'), nullable=False)
    prompt = Column(Text)
    datahora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="promptusuario")

class Politica(Base):
    __tablename__ = 'tb_politicas'
    __table_args__ = {'schema': 'p2'}
    
    politicaid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    permissao = Column(String(20), nullable=False)
    descricao = Column(String(100), nullable=False)

    # Relacionamentos
    permissao1 = relationship("Permissao", back_populates="politica")

class Tipo(Base):
    __tablename__ = 'tb_tipos'
    __table_args__ = {'schema': 'p2'}
    
    tipoid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    tipo = Column(String(15), nullable=False)

    # Relacionamentos
    permissoes = relationship("Permissao", back_populates="tipo")
    usuario = relationship("Usuario", back_populates="tipou")

class Permissao(Base):
    __tablename__ = 'tb_permissoes'
    __table_args__ = {'schema': 'p2'}
    
    permissaoid = Column(Integer, Identity(start=1), primary_key=True, index=True)
    tipoid = Column(Integer, ForeignKey('p2.tb_tipos.tipoid'), nullable=False)
    politicaid = Column(Integer, ForeignKey('p2.tb_politicas.politicaid'), nullable=False)

    # Relacionamentos
    tipo = relationship("Tipo", back_populates="permissoes")    
    politica = relationship("Politica", back_populates="permissao1")    