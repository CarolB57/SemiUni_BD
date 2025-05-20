-- PERGUNTAS FREQUENTES

INSERT INTO PerguntasFrequentes(Codigo, Pergunta, Resposta)
VALUES (0001, 'Tentei me cadastrar e aparece a mensagem: CPF já cadastrado.', 'Tente recuperar a senha. 
Verifique se e-mail de recuperação de senha não foi enviado para sua caixa de lixeira ou SPAM.'),
	   (0002, 'Não consigo efetuar login.', 'Verifique se seus dados estão de acordo com as informações 
pessoais contidas no Matrícula Web e tente recuperar a senha. Se os procedimentos anteriores não tiverem 
funcionado entre em contato com o Decanato de Extensão pelo e-mail semanauniversitariaunb@gmail.com com o título: 
[SIEX] Não consigo efetuar o login, no corpo de e-mail de ve constar seu nome completo; CPF; matrícula e e-mail 
cadastrado no matricula web.'),
       (0003, 'Onde posso acessar a programação?', 'Acesse o site Unb Decanato de Extensão (DEX) e procure pela 
programação na primeira página do site. Dica: após fazer o download da programação da #Semuni2025, faça uma busca 
(CRTL +F) com palavras-chave de seu interesse!'),
	   (0004, 'Como fazer a inscrição nas atividades?', 'Acesse o site oficial da UnB e clique na opção inscrições, 
no menu lateral. Dentro dessa página, selecionar “Tipo Ação” Semana Universitária.'),
	   (0005, 'Como faço para tirar minha inscrição de alguma atividade?', 'Não há cancelamento de inscrição.');


-- DEPARTAMENTO

INSERT INTO Departamento(Codigo, Nome)
VALUES ('CIC', 'Departamento de Ciência da Computação'),
	   ('ENP', 'Departamento de Engenharia de Produção'),
	   ('ENC', 'Departamento de Engenharia Civil'),
       ('ENE', 'Departamento de Engenharia Elétrica'),
	   ('SOL', 'Departamento de Sociologia');


-- CURSO

INSERT INTO Curso(Codigo, Nome, Tipo, Cod_Departamento)
VALUES (746331003, 'Ciência da Computação','Licenciatura','CIC'),
	   (993746282, 'Engenharia de Produção', 'Bacharelado', 'ENP'),
	   (546378728, 'Sociologia', 'Bacharelado', 'SOL'),
       (298234736, 'Engenharia Elétrica', 'Bacharelado', 'ENE'),
	   (873648364, 'Engenharia Civil', 'Bacharelado', 'ENC');


-- PARTICIPANTE

INSERT INTO Participante(CPF, Nome, Ocupacao, Email, Cod_curso)
VALUES ('37487313393', 'Minatozaki Sana','Aluna','sanaminatozaki293@aluno.unb.br', '746331003'),
	   ('63729238111', 'Myoui Mina', 'Palestrante', 'minasharonmyoui@jyp.com', NULL),
	   ('74829223203', 'Park Jihyo', 'Visitante', 'jihyo_zyoo@jyp.com', NULL),
       ('32528123433', 'Son Chaeyoung', 'Professora', 'strawberrychaeyoung@unb.br', '993746282'),
	   ('49201956399', 'Yoo Jeongyeon', 'Professora', 'tenis_jeong@unb.br', '298234736');

INSERT INTO Telefone(CPF_participante, Fone)
VALUES ('37487313393', '64984321923'),
	   ('37487313393', '64993421666'),
	   ('74829223203', '62997523422'),
       ('32528123433', '61998538273'),
	   ('49201956399', '61996541029');


-- TIPOATIVIDADE

INSERT INTO TipoAtividade(Codigo, Nome)
VALUES (9857, 'WORKSHOP'),
	   (5354, 'FEIRA'),
	   (9865, 'PALESTRA'),
       (4442, 'OFICINA'),
	   (2224, 'JORNADA');


-- LOCALATIVIDADE

INSERT INTO LocalAtividade(Codigo, Nome, Sigla, Capacidade)
VALUES (34525, 'Prédio ICC Módulo 19 - Laboratório de Informática (subsolo) - Campus Darcy Ribeiro/UnB', 'ICC', 50),
	   (23452, 'Bloco UAC - FGA/UnB', 'UAC', 200),
	   (54632, 'Sala i04 UAC - FGA/UnB', 'UAC', 100),
       (42452, 'Sala i06 UAC - FGA/UnB', 'UAC', 20),
	   (55673, 'Sala i08 UAC - FGA/UnB', 'FGA', 70);


-- ATIVIDADE

INSERT INTO Atividade(Codigo, Tema, Cod_TipoAti, Descricao, Programacao, DataInicio, DataFim, HorarioInicio, HorarioFim, CargaHoraria, Vagas, Cod_Local) 
VALUES (839201, 'Game Jam 2025', 9857, 'Pequena competição com grupos de cerca de 4 pessoas que procuram desenvolver um protótipo de um jogo eletrônico ao longo 
de uma semana de trabalho, 4 horas por dia. O tema desta Game Jam será "Esportes Olímpicos".', 
'Segunda-feira: Primeiro encontro dos participantes, explicação das 
regras, formação de grupos e início do desenvolvimento;
Terça-feira a quinta-feira: Encontros dedicados ao desenvolvimento dos jogos;
Sexta-feira: Finalização do evento e premiação.', '2025-11-10', '2025-11-14', '14:00', '18:00', 20, 40, 34525),
	   (573920, 'Feira de Inovação Tecnológica (FIT) da Faculdade UnB Gama', 5354, 'Apresentar à comunidade acadêmica e à comunidade externa, os projetos de Inovação 
	   e Engenharia desenvolvidos pelos estudantes de graduação no âmbito das disciplinas que compõe os 5 cursos de graduação ofertados pela Faculdade UnB Gama, a saber: 
	   Engenharia de Energia, Automotiva, Eletrônica, Aeroespacial e de Software.', 'Apresentação de Trabalhos - Projeto Integrador de Engenharias 2.', '2025-11-12', 
	   '2025-11-12', '10:00', '17:00', 8, 200, 23452),
	   (675849, 'Mesa de Abertura SEMUNI 2025', 9865, 'Atividade voltada para o início das ações a serem realizadas na Semana Universitária (SEMUNI) da Faculdade do Gama 
	   (FGA). Tem por iniciativa apresentar a Extensão da UnB e da FGA, bem como destacar as ações realizadas pelos cinco cursos do Campus. Visa apresentar a SEMUNI aos 
	   estudantes universitários e aos alunos de ensino fundamental e médio.', 'Boas-vindas;
	   Apresentação do Diretor e Vice-diretor;
	   Apresentação do coordenador acadêmico da FGA;
	   Apresentação do coordenador do curso Engenharia Aeroespacial;
	   Apresentação do coordenador do curso Engenharia Automotiva;
	   Apresentação do coordenador do curso Engenharia Eletrônica;
	   Apresentação do coordenador do curso Engenharia de Energia;
	   Apresentação do coordenador do curso Engenharia de Software;
	   Interação com o público;
	   Início das atividades da SEMUNI 2024;
	   Coffe break.', '2025-11-11', '2025-11-11', '10:00', '11:00', 1, 100, 54632),
       (394754, 'Edubot - Oficina de Robótica Móvel', 4442, 'Ensinar gratuitamente robótica móvel para alunos de escolas públicas de nível médio em Brasília utilizando o 
	   robô educacional Sparki e realizará um workshop durante a semana universitária com o intuito de demonstrar e colocar em prática o ensino básico de robótica móvel, 
	   explorando e aprofundando o funcionamento do Sparki, com o objetivo de introduzir noções fundamentais de robótica móvel. A principal atividade a ser realizada será o 
	   Projeto de Limpeza, no qual o Sparki posicionado dentro de um quadrado com objetos a pelo menos 30 centimêtros de distância, detectará e removerá esses itens para 
	   fora do quadrado. Paralelamente, será feita uma explicação complementar sobre o funcionamento interno do robô, abordando suas engrenagens, sensores e motores.', 
	   'Introdução ao Projeto Edubot, ao Sparki e à equipe de membros do projeto; 
       Introdução ao Sparkiduino e sua documentação;
	   Introdução aos componentes do Sparki;
	   Utilizando os motores e garras;
	   Finalização do código do Projeto Robô de Limpeza;', '2025-11-12', '2025-11-13', '14:00', '16:00', 20, 40, 42452),
	   (938475, 'COPA DAS EDOS NAS ESTAÇÕES', 2224, 'Campeonato temático onde os alunos competem em resolver equações diferenciais ordinárias de 1ª e 2ª ordem, passando 
	   por desafios representados pelas quatro estações do ano: Primavera, Verão, Outono e Inverno. Cada estação representa um conjunto de problemas com diferentes níveis 
	   de dificuldade, e os alunos acumulam pontos à medida que avançam e aprendem a trabalhar em grupo (colaborativismo).', 
	   '14h-14h30: Apresentação das regras; Divisão dos grupos em estações. 
	   14h30-15h45: Etapa 1: Cartas nível: básicas e intermediárias 
	   15h45-16h: Intervalo 
	   16h-17h45: Etapa 2: Cartas nível: moderado e desafiadoras. 
	   17h45-18h: Fechamento do evento', '2025-11-14', '2025-11-14', '14:00', '18:00', 8, 65, 55673);


-- INSCRICAO

INSERT INTO Inscricao(Codigo, Cod_Atividade, CPF_Participante, DataIncricao, Presenca)
VALUES (73647823, 839201, '37487313393', '2025-11-04', TRUE),
	   (29247249, 675849, '49201956399', '2025-11-05', FALSE),
	   (84738292, 394754, '74829223203', '2025-11-07', TRUE),
       (85739326, 938475, '37487313393', '2025-11-03', TRUE),
	   (75648322, 675849, '74829223203', '2025-11-09', FALSE);


-- CERTIFICADO

INSERT INTO Certificado(Codigo, Cod_Inscricao, Tipo, Emitido, DataEmissao)
VALUES (7382642, 73647823, 'Participação', TRUE, '2025-11-16'),
	   (1927583, 29247249, 'Participação', TRUE, '2025-11-12'),
	   (1028473, 84738292, 'Participação', FALSE, NULL),
       (1093725, 85739326, 'Ministrante Evento', FALSE, NULL),
	   (1029383, 75648322, 'Ministrante Palestra', TRUE, '2025-11-12');


-- FEEDBACK

INSERT INTO Feedback(Codigo, Cod_Inscricao, Nota, Comentario)
VALUES (7382, 73647823, 10, 'O evento Game Jam é geralmente um evento muito divertido, e esse ano não foi diferente. A organização estava muito boa e o tema desse ano foi 
muito interessante. Gostei bastante!'),
	   (1927, 29247249, 10, 'A Mesa de Abertura da Semana Universitária foi muito legal. A fala dos diretores foi bem interessante. A melhor parte foi o Coffee Break 
	   com lanchinho!'),
	   (1028, 84738292, 5, 'O evento Edubot foi super mal organizado. Foi um evento em que os organizadores simplesmente atrasaram tudo e não conseguiram realmente 
	   conduzir o evento. Tomara que ano que vem a organização mude, pois esse ano foi horrível!'),
       (9372, 85739326, 8, 'O evento da Copa das EDOS foi divertido, mas deveriam melhorar a estrutura das salas para maior conforto dos alunos.'),
	   (1938, 75648322, NULL, NULL);

