-- Políticas
INSERT INTO p2.tb_politicas
(permissao, descricao)
VALUES('USR:ADMIN', 'Permissão de Administrador do Cadastro de Usuários');

INSERT INTO p2.tb_politicas
(permissao, descricao)
VALUES('USR:ESCRITA', 'Permissão de Escrita do Cadastro de Usuários');

INSERT INTO p2.tb_politicas
(permissao, descricao)
VALUES('USR:LEITURA', 'Permissão de Leitura do Cadastro de Usuários');

INSERT INTO p2.tb_politicas
(permissao, descricao)
VALUES('PRJ:ADMIN', 'Permissão de Administrador do Cadastro de Projetos');

INSERT INTO p2.tb_politicas
(permissao, descricao)
VALUES('PRJ:ESCRITA', 'Permissão de Escrita do Cadastro de Projetos');

INSERT INTO p2.tb_politicas
(permissao, descricao)
VALUES('PRJ:LEITURA', 'Permissão de Leitura do Cadastro de Projetos');

--Tipos
INSERT INTO p2.tb_tipos
(tipo)
VALUES('Administrador');

INSERT INTO p2.tb_tipos
(tipo)
VALUES('Supervisor');

INSERT INTO p2.tb_tipos
(tipo)
VALUES('Usuário');

-- Permissões
INSERT INTO p2.tb_permissoes
(tipoid, politicaid)
VALUES(1, 1);

INSERT INTO p2.tb_permissoes
(tipoid, politicaid)
VALUES(1, 4);

INSERT INTO p2.tb_permissoes
(tipoid, politicaid)
VALUES(2, 5);

INSERT INTO p2.tb_permissoes
(tipoid, politicaid)
VALUES(3, 6);

-- Usuários
INSERT INTO p2.tb_usuarios
(email, senha, nome, tipoid, status)
VALUES('msrs@cesar.school', '$2b$12$OvvHOu3reWflGL/3vxIA7OU6f.k6ZqHctR.S/euFWY8W6eTTHdakm', 'Mauro Sérgio Rezende da Silva', 1, 'Ativo');

INSERT INTO p2.tb_usuarios
(email, senha, nome, tipoid, status)
VALUES('atlc@cesar.school', 'Hash', 'Artur Torres Lima Cavalcanti', 1, 'Ativo');

INSERT INTO p2.tb_usuarios
(email, senha, nome, tipoid, status)
VALUES('cvaf@cesar.school', 'Hash', 'Carlos Vinicius Alves de Figueiredo', 1, 'Ativo');

INSERT INTO p2.tb_usuarios
(email, senha, nome, tipoid, status)
VALUES('ehffb@cesar.school', 'Hash', 'Eduardo Henrique Ferreira Fonseca Barbosa', 1, 'Ativo');

INSERT INTO p2.tb_usuarios
(email, senha, nome, tipoid, status)
VALUES('gma@cesar.school', 'Hash', 'Gabriel de Medeiros Almeida', 1, 'Ativo');

INSERT INTO p2.tb_usuarios
(email, senha, nome, tipoid, status)
VALUES('sbt@cesar.school', 'Hash', 'Silvio Barros Tenório', 1, 'Ativo');

-- Projetos
INSERT INTO p2.tb_projetos
(projeto, status)
VALUES('Retalho Alimentar', 'Ativo');

INSERT INTO p2.tb_projetos
(projeto, status)
VALUES('Saúde e Bem-Estar', 'Ativo');

INSERT INTO p2.tb_projetos
(projeto, status)
VALUES('Negócios Complementares de Retalho', 'Ativo');

-- Prompt Geral
INSERT INTO p2.tb_prompt_geral
(prompt, usuarioid, datahora)
VALUES('--- REGRAS FUNDAMENTAIS ---
    1.  Sua resposta deve se basear *ESTRITA E EXCLUSIVAMENTE* no conteúdo dos textos fornecidos no bloco "texto bruto dos documentos".
    2.  É *PROIBIDO* buscar ou inferir qualquer informação externa da internet ou de seu conhecimento prévio.
    3.  Se um documento não contiver informações suficientes para preencher uma seção (como a tabela) ou para atender ao foco do usuário, preencha a seção correspondente com a frase *"Informação Não Processada"*. Não invente ou deduza dados.
    4.  A geração de uma tabela de dados para cada documento é *OBRIGATÓRIA*.
22h33
Coloquei essas regras no prompt
22h33
E retirei aquele resumão de todos os documentos', 1, NOW());
