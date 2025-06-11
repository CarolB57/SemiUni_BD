CREATE TABLE Departamento(
    Codigo VARCHAR(3) PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL
);

CREATE TABLE Curso(
    Codigo INTEGER PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL,
    Tipo VARCHAR(30) NOT NULL,
    Cod_Departamento VARCHAR(3),
    FOREIGN KEY (Cod_Departamento) REFERENCES Departamento(Codigo)
);

CREATE TABLE Participante(
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL,
    Ocupacao VARCHAR(40) NOT NULL,
    Email VARCHAR(30),
    Cod_curso INTEGER,
    FOREIGN KEY (Cod_curso) REFERENCES Curso(Codigo)
);

CREATE TABLE Telefone(
    CPF_participante VARCHAR(11),
    Fone VARCHAR(11),
    PRIMARY KEY (CPF_participante, Fone),
    FOREIGN KEY (CPF_participante) REFERENCES Participante(CPF)
);

CREATE TABLE TipoAtividade(
    Codigo INTEGER PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL
);

CREATE TABLE LocalAtividade(
    Codigo INTEGER PRIMARY KEY,
    Nome VARCHAR(180) NOT NULL,
    Sigla VARCHAR(3) NOT NULL,
    Capacidade INTEGER
);

CREATE TABLE Atividade(
    Codigo INTEGER PRIMARY KEY,
    Tema VARCHAR(60) NOT NULL,
    Cod_TipoAti INTEGER,
    Descricao TEXT,
    Programacao TEXT,
    DataInicio DATE,
    DataFim DATE,
    HorarioInicio TIME,
    HorarioFim TIME,
    CargaHoraria INTEGER,
    Vagas INTEGER,
    Cod_Local INTEGER,
    FOREIGN KEY (Cod_TipoAti) REFERENCES TipoAtividade(Codigo),
    FOREIGN KEY (Cod_Local) REFERENCES LocalAtividade(Codigo)
);

CREATE TABLE Inscricao(
    Codigo INTEGER PRIMARY KEY,
    Cod_Atividade INTEGER,
    CPF_Participante VARCHAR(11),
    DataIncricao DATE,
    Presenca BOOLEAN NOT NULL,
    FOREIGN KEY (Cod_Atividade) REFERENCES Atividade(Codigo),
    FOREIGN KEY (CPF_Participante) REFERENCES Participante(CPF)
);

CREATE TABLE Certificado(
    Codigo INTEGER PRIMARY KEY,
    Cod_Inscricao INTEGER,
    Tipo VARCHAR(30),
    Emitido BOOLEAN,
    DataEmissao DATE,
    FOREIGN KEY (Cod_Inscricao) REFERENCES Inscricao(Codigo)
);

CREATE TABLE Feedback(
    Codigo INTEGER PRIMARY KEY,
    Cod_Inscricao INTEGER,
    Nota INTEGER CHECK (Nota BETWEEN 1 AND 10),
    Comentario TEXT,
    FOREIGN KEY (Cod_Inscricao) REFERENCES Inscricao(Codigo)
);

CREATE TABLE PerguntasFrequentes(
    Codigo INTEGER PRIMARY KEY,
    Pergunta TEXT,
    Resposta TEXT
);
