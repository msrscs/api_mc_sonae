# Faculdade 
    Cesar School

# Curso
    Segurança da Informação

# Período
    2025.2

# Disciplina
    Projeto 2

# Professor de Projeto 2
    Marlon Silva Ferreira

# Professor de Programação Orientada a Objeto
    João Victor Tinoco de Souza Abreu

# Equipe
    Artur Torres Lima Cavalcanti
    Carlos Vinicius Alves de Figueiredo
    Eduardo Henrique Ferreira Fonseca Barbosa
    Gabriel de Medeiros Almeida
    Mauro Sérgio Rezende da Silva
    Silvio Barros Tenório

# Projeto
    Automatizar a criação de conteúdos para comunicar projetos e respectivos resultados.

# Cliente
    MC Sonae

# Comandos
    - Cria ambiente virtual
        python -m venv venv

    - Ativar ambiente virtual
        * Linux/Mac:
            source venv/bin/activate
        * Windows:
            venv/Scripts/activate

    - Atualizar o pip
        python.exe -m pip install --upgrade pip

    - Lista os pacotes instalados
        pip freeze

    - Gerar arquivo requirements.txt
        pip freeze > requirements.txt

    - Recuperar venv com requirements.txt
        pip install -r ./requirements.txt

    - Instalar as Bibliotecas
        + Fast API
          pip install "fastapi[all]"
        + SQL Alchemy (Mapeador Relacional de Objetos)
          pip install sqlalchemy
        + Psycopg (Adaptador de banco de dados PostgreSQL)  
          pip install psycopg2-binary
        + JavaScript Object Signing and Encryption (JOSE) - JSON Web Tokens (JWT)
          pip install "python-jose[cryptography]"
        + Bcrypt (Gerador do Hash da senha)
          pip install bcrypt
        + Dotenv (Ambiente variáveis - Lê pares de valores-chave de um arquivo .env)
          pip install python-dotenv
            
# Arquivos Python
    - main.py                   => Arquivo main da Api MC Sonae 
    - auth.py                   => Autenticação JWT
    - crud.py                   => Crud do Banco de Dados
    - database.py               => Conexão do Banco de Dados
    - models.py                 => Modelos das Classes
    - schemas.py                => Esquemas Pydantic
    - auth_router.py            => Rota de Autenticação
    - permissao_router.py       => Rota de Permissão
    - politica_router.py        => Rota de Política
    - projetos_router.py        => Rota de Projetos
    - prompt_geral_router.py    => Rota de Prompt Geral
    - prompt_usuario_router.py  => Rota de Prompt Usuário
    - repositorio_router.py     => Rota de Repositório
    - tipo_router.py            => Rota de Tipo
    - usuarios_router.py        => Rota de Usuários

# Arquivos de Script Banco de Dados
    - script_bd_mcsonae.sql     => Criação do Banco de Dados bd_mcsonae
    - script_popula.sql         => População Inicial do Banco de Dados

# Executar API
    uvicorn app.main:app --reload
