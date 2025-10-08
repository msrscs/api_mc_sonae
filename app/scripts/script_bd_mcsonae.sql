-- DROP TABLE p2.tb_usuarios;

CREATE TABLE p2.tb_usuarios (
	usuarioid int GENERATED ALWAYS AS IDENTITY NOT NULL,
	email varchar(100) NOT NULL,
	senha varchar(255) NOT NULL,
	nome varchar(50) NOT NULL,
	tipoid int NOT NULL,
	status varchar(15) NOT NULL,
	CONSTRAINT tb_usuarios_email_key UNIQUE (email),
	CONSTRAINT tb_usuarios_pkey PRIMARY KEY (usuarioid)
);

--DROP TABLE p2.tb_projetos;

CREATE TABLE p2.tb_projetos (
        projetoid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        projeto varchar(100) NOT NULL,
        status varchar(15) NOT NULL,
	CONSTRAINT tb_projetos_projeto_key UNIQUE (projeto),
        CONSTRAINT tb_projetos_pkey PRIMARY KEY (projetoid)
);

--DROP TABLE p2.tb_repositorio_pj;

CREATE TABLE p2.tb_repositorio_pj (
        repositorioid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        projetoid int NOT NULL,
        usuarioid int NOT NULL,
        markdown text NULL,
        datahora timestamptz NOT NULL,
        CONSTRAINT tb_repositorio_pkey PRIMARY KEY (repositorioid)
);

--DROP TABLE p2.tb_prompt_geral;

CREATE TABLE p2.tb_prompt_geral (
        promptid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        prompt text NULL,
        usuarioid int NOT NULL,
        datahora timestamptz NOT NULL,
        CONSTRAINT tb_prompt_geral_pkey PRIMARY KEY (promptid)
);

--DROP TABLE p2.tb_prompt_usuario;

CREATE TABLE p2.tb_prompt_usuario (
        promptid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        usuarioid int NOT NULL,
        prompt text NULL,
        datahora timestamptz NOT NULL,
        CONSTRAINT tb_prompt_usuario_pkey PRIMARY KEY (promptid)
);

--DROP TABLE p2.tb_tipos;

CREATE TABLE p2.tb_tipos (
        tipoid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        tipo varchar(15) NOT NULL,
	CONSTRAINT tb_tipos_tipo_key UNIQUE (tipo),
        CONSTRAINT tb_tipos_pkey PRIMARY KEY (tipoid)
);

--DROP TABLE p2.tb_permissoes;

CREATE TABLE p2.tb_permissoes (
        permissaoid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        tipoid int NOT NULL,
        politicaid int NOT NULL,
	CONSTRAINT tb_tipos_politica_tipo_key UNIQUE (tipoid, politicaid),
        CONSTRAINT tb_permissoes_pkey PRIMARY KEY (permissaoid)
);

--DROP TABLE p2.tb_politicas;

CREATE TABLE p2.tb_politicas (
        politicaid int GENERATED ALWAYS AS IDENTITY NOT NULL,
        permissao varchar(20) NOT NULL,
        descricao varchar(100) NOT NULL,
	CONSTRAINT tb_politicas_permissao_key UNIQUE (permissao),
        CONSTRAINT tb_politicas_pkey PRIMARY KEY (politicaid)
);
