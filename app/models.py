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
# Data: 20/10/2025                                      #
######################################################### 

import re
from wsgiref import validate
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Identity
from sqlalchemy.orm import relationship, validates, synonym
from sqlalchemy.sql import func
from .database import Base
from fastapi import HTTPException

class Usuario(Base):
    __tablename__ = 'tb_usuarios'
    __table_args__ = {'schema': 'p2'}

    _usuarioid = Column("usuarioid", Integer, Identity(start=1), primary_key=True, index=True)
    _email = Column("email", String(100), unique=True, nullable=False, index=True)
    _senha = Column("senha", String(255), nullable=False)
    _nome = Column("nome", String(50), nullable=False)
    _tipoid = Column("tipoid", Integer, ForeignKey('p2.tb_tipos.tipoid'), nullable=False)
    _status = Column("status", String(15), nullable=False)

    @property
    def usuarioid(self):
        return self._usuarioid

    # @usuarioid.setter
    # def usuarioid(self, value):
    #     self._usuarioid = value
   
    usuarioid = synonym('_usuarioid', descriptor=usuarioid)  # type: ignore

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise HTTPException(status_code=400, detail="Endereço de email inválido.")
        self._email = value

    email = synonym('_email', descriptor=property(email.fget, email.fset))  # type: ignore

    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, value):
        if len(value) < 12:
            raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 12 caracteres.")
        self._senha = value

    senha = synonym('_senha', descriptor=property(senha.fget, senha.fset))  # type: ignore

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
        self._nome = value

    nome = synonym('_nome', descriptor=property(nome.fget, nome.fset))  # type: ignore

    @property
    def tipoid(self):
        return self._tipoid
    
    @tipoid.setter
    def tipoid(self, value):
        self._tipoid = value

    tipoid = synonym('_tipoid', descriptor=property(tipoid.fget, tipoid.fset))  # type: ignore

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        STATUS_VALIDOS = ['Ativo', 'Bloqueado', 'Cancelado']
        if value not in STATUS_VALIDOS: 
            raise HTTPException(status_code=400, detail=f"Status {value} inválido. Valores permitidos: {', '.join(STATUS_VALIDOS)}")
        self._status = value

    status = synonym('_status', descriptor=property(status.fget, status.fset))  # type: ignore

    # Relacionamentos
    promptgeral = relationship("PromptGeral", back_populates="usuario")
    promptusuario = relationship("PromptUsuario", back_populates="usuario")
    repositorios = relationship("Repositorio", back_populates="usuario")
    tipou = relationship("Tipo", back_populates="usuario")

class Projeto(Base):
    __tablename__ = 'tb_projetos'
    __table_args__ = {'schema': 'p2'}

    _projetoid = Column("projetoid", Integer, Identity(start=1), primary_key=True, index=True)
    _projeto = Column("projeto", String(100), nullable=False)
    _status = Column("status", String(15), nullable=False)
    
    @property
    def projetoid(self):
        return self._projetoid
    
    # @projetoid.setter
    # def projetoid(self, value):
    #     self._projetoid = value

    projetoid = synonym('_projetoid', descriptor=projetoid)  # type: ignore

    @property
    def projeto(self):
        return self._projeto
    
    @projeto.setter
    def projeto(self, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="O nome do projeto não pode estar vazio.")
        self._projeto = value

    projeto = synonym('_projeto', descriptor=property(projeto.fget, projeto.fset))  # type: ignore

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        STATUS_VALIDOS = ['Ativo', 'Encerrado']
        if value not in STATUS_VALIDOS:
            raise HTTPException(status_code=400, detail=f"Status {value} inválido. Valores permitidos: {', '.join(STATUS_VALIDOS)}")
            # raise ValueError(f"Status {value} inválido. Valores permitidos: {', '.join(STATUS_VALIDOS)}")
        self._status = value

    status = synonym('_status', descriptor=property(status.fget, status.fset))  # type: ignore

    # Relacionamentos
    repositorios = relationship("Repositorio", back_populates="projeto")

class Repositorio(Base):
    __tablename__ = 'tb_repositorio_pj'
    __table_args__ = {'schema': 'p2'}

    _repositorioid = Column("repositorioid", Integer, Identity(start=1), primary_key=True, index=True)
    _projetoid = Column("projetoid", Integer, ForeignKey('p2.tb_projetos.projetoid'), nullable=False)
    _usuarioid = Column("usuarioid", Integer, ForeignKey('p2.tb_usuarios.usuarioid'), nullable=False)
    _tipoarquivo = Column("tipoarquivo", String(5), nullable=False)
    _markdown = Column("markdown", Text)
    _datahora = Column("datahora", DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def repositorioid(self):
        return self._repositorioid 
    
    # @repositorioid.setter
    # def repositorioid(self, value):
    #     self._repositorioid = value 

    repositorioid = synonym('_repositorioid', descriptor=repositorioid)  # type: ignore

    @property
    def projetoid(self):
        return self._projetoid

    @projetoid.setter
    def projetoid(self, value):
        self._projetoid = value
    
    projetoid = synonym('_projetoid', descriptor=property(projetoid.fget, projetoid.fset))  # type: ignore

    @property
    def usuarioid(self):
        return self._usuarioid
    
    @usuarioid.setter
    def usuarioid(self, value):
        self._usuarioid = value
    
    usuarioid = synonym('_usuarioid', descriptor=property(usuarioid.fget, usuarioid.fset))  # type: ignore

    @property
    def tipoarquivo(self):
        return self._tipoarquivo
    
    @tipoarquivo.setter
    def tipoarquivo(self, value):
        TIPOS_VALIDOS = ['pdf', 'doc', 'docx', 'xls', 'xlsx'] 
        if value not in TIPOS_VALIDOS:
            raise HTTPException(status_code=400, detail=f"Tipo de arquivo {value} inválido. Valores permitidos: {', '.join(TIPOS_VALIDOS)}")
        self._tipoarquivo = value
    
    tipoarquivo = synonym('_tipoarquivo', descriptor=property(tipoarquivo.fget, tipoarquivo.fset))  # type: ignore

    @property
    def markdown(self):
        return self._markdown
    
    @markdown.setter
    def markdown(self, value):
        self._markdown = value
    
    markdown = synonym('_markdown', descriptor=property(markdown.fget, markdown.fset))  # type: ignore

    @property
    def datahora(self):
        return self._datahora
    
    @datahora.setter
    def datahora(self, value):
        self._datahora = value
    
    datahora = synonym('_datahora', descriptor=property(datahora.fget, datahora.fset))  # type: ignore

    # Relacionamentos
    projeto = relationship("Projeto", back_populates="repositorios")
    usuario = relationship("Usuario", back_populates="repositorios")

class PromptGeral(Base):
    __tablename__ = 'tb_prompt_geral'
    __table_args__ = {'schema': 'p2'}
    
    _promptid = Column("promptid", Integer, Identity(start=1), primary_key=True, index=True)
    _prompt = Column("prompt", Text)
    _usuarioid = Column("usuarioid", Integer, ForeignKey('p2.tb_usuarios.usuarioid'), nullable=False)
    _datahora = Column("datahora", DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def promptid(self):
        return self._promptid

    # @promptid.setter
    # def promptid(self, value):
    #     self._promptid = value

    promptid = synonym('_promptid', descriptor=promptid)  # type: ignore

    @property
    def prompt(self):
        return self._prompt
    
    @prompt.setter
    def prompt(self, value):
        self._prompt = value

    prompt = synonym('_prompt', descriptor=property(prompt.fget, prompt.fset))  # type: ignore

    @property
    def usuarioid(self):
        return self._usuarioid
    
    @usuarioid.setter
    def usuarioid(self, value):
        self._usuarioid = value
    
    usuarioid = synonym('_usuarioid', descriptor=property(usuarioid.fget, usuarioid.fset))  # type: ignore

    @property
    def datahora(self):
        return self._datahora
    
    @datahora.setter
    def datahora(self, value):
        self._datahora = value
    
    datahora = synonym('_datahora', descriptor=property(datahora.fget, datahora.fset))  # type: ignore

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="promptgeral")

class PromptUsuario(Base):
    __tablename__ = 'tb_prompt_usuario'
    __table_args__ = {'schema': 'p2'}
    
    _promptid = Column("promptid", Integer, Identity(start=1), primary_key=True, index=True)
    _usuarioid = Column("usuarioid", Integer, ForeignKey('p2.tb_usuarios.usuarioid'), nullable=False)
    _prompt = Column("prompt", Text)
    _datahora = Column("datahora", DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def promptid(self):
        return self._promptid
    
    # @promptid.setter
    # def promptid(self, value):
    #     self._promptid = value
    
    promptid = synonym('_promptid', descriptor=promptid)  # type: ignore

    @property
    def usuarioid(self):
        return self._usuarioid
    
    @usuarioid.setter
    def usuarioid(self, value):
        self._usuarioid = value
    
    usuarioid = synonym('_usuarioid', descriptor=property(usuarioid.fget, usuarioid.fset))  # type: ignore

    @property
    def prompt(self):
        return self._prompt
    
    @prompt.setter
    def prompt(self, value):
        self._prompt = value
    
    prompt = synonym('_prompt', descriptor=property(prompt.fget, prompt.fset))  # type: ignore

    @property
    def datahora(self):
        return self._datahora
    
    @datahora.setter
    def datahora(self, value):
        self._datahora = value

    datahora = synonym('_datahora', descriptor=property(datahora.fget, datahora.fset))  # type: ignore

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="promptusuario")

class Politica(Base):
    __tablename__ = 'tb_politicas'
    __table_args__ = {'schema': 'p2'}
    
    _politicaid = Column("politicaid", Integer, Identity(start=1), primary_key=True, index=True)
    _permissao = Column("permissao", String(20), nullable=False)
    _descricao = Column("descricao", String(100), nullable=False)

    @property
    def politicaid(self):
        return self._politicaid
    
    # @politicaid.setter
    # def politicaid(self, value):
    #     self._politicaid = value

    politicaid = synonym('_politicaid', descriptor=politicaid)  # type: ignore

    @property
    def permissao(self):
        return self._permissao
    
    @permissao.setter
    def permissao(self, value):
        self._permissao = value
    
    permissao = synonym('_permissao', descriptor=property(permissao.fget, permissao.fset))  # type: ignore

    @property
    def descricao(self):
        return self._descricao
    
    @descricao.setter
    def descricao(self, value):
        self._descricao = value
    
    descricao = synonym('_descricao', descriptor=property(descricao.fget, descricao.fset))  # type: ignore
    
    # Relacionamentos
    permissao1 = relationship("Permissao", back_populates="politica")

class Tipo(Base):
    __tablename__ = 'tb_tipos'
    __table_args__ = {'schema': 'p2'}
    
    _tipoid = Column("tipoid", Integer, Identity(start=1), primary_key=True, index=True)
    _tipo = Column("tipo", String(15), nullable=False)

    @property
    def tipoid(self):
        return self._tipoid
    
    # @tipoid.setter
    # def tipoid(self, value):
    #     self._tipoid = value

    tipoid = synonym('_tipoid', descriptor=tipoid)  # type: ignore

    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    tipo = synonym('_tipo', descriptor=property(tipo.fget, tipo.fset))  # type: ignore

    # Relacionamentos
    permissoes = relationship("Permissao", back_populates="tipo")
    usuario = relationship("Usuario", back_populates="tipou")

class Permissao(Base):
    __tablename__ = 'tb_permissoes'
    __table_args__ = {'schema': 'p2'}
    
    _permissaoid = Column("permissaoid", Integer, Identity(start=1), primary_key=True, index=True)
    _tipoid = Column("tipoid", Integer, ForeignKey('p2.tb_tipos.tipoid'), nullable=False)
    _politicaid = Column("politicaid", Integer, ForeignKey('p2.tb_politicas.politicaid'), nullable=False)

    @property
    def permissaoid(self):
        return self._permissaoid
    
    # @permissaoid.setter
    # def permissaoid(self, value):
    #     self._permissaoid = value

    permissaoid = synonym('_permissaoid', descriptor=permissaoid)  # type: ignore
    
    @property
    def tipoid(self):
        return self._tipoid
    
    @tipoid.setter
    def tipoid(self, value):
        self._tipoid = value
    
    tipoid = synonym('_tipoid', descriptor=property(tipoid.fget, tipoid.fset))  # type: ignore

    @property
    def politicaid(self):
        return self._politicaid
    
    @politicaid.setter
    def politicaid(self, value):
        self._politicaid = value

    politicaid = synonym('_politicaid', descriptor=property(politicaid.fget, politicaid.fset))  # type: ignore

    # Relacionamentos
    tipo = relationship("Tipo", back_populates="permissoes")    
    politica = relationship("Politica", back_populates="permissao1")    