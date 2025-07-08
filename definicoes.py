'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

import re
import random
import textwrap
import tkinter as tk
from tkinter import Tk
from database import *
from dicionario import *
from psycopg2 import Binary
from rich.panel import Panel
from tabulate import tabulate
from tkinter import filedialog
from rich.console import Console
from tkinter.filedialog import askopenfilename
from datetime import datetime, date, timedelta, time


def email_valido(email):
    if "@" not in email or "." not in email:
        return False
    arroba = email.index("@")
    ponto = email.rindex(".")
    return 0 < arroba < ponto < len(email) - 1

def limpar_cpf(cpf):
    return cpf.replace(".", "").replace("-", "")

def cpf_valido(cpf):
    return cpf.isdigit() and len(cpf) == 11

def nome_valido(nome):
    nome = nome.strip()
    
    if len(nome) < 2:
        return False
    
    # Verifica se só tem letras e espaços
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
        return False
    
    return True

def normalizar_nome(nome):
    return ' '.join(p.capitalize() for p in nome.strip().split())

def ocupacao_valida(ocupacao):
    return ocupacao in ['visitante', 'palestrante', 'professor', 'professora', 'aluno', 'aluna']

def tipo_valido(tipo_certificado):
    return tipo_certificado in ['participação', 'ministrante evento', 'ministrante palestra']

def limpar_telefone(fone: str) -> str:  #Remove todos os caracteres não numéricos de um telefone.
    return re.sub(r'\D', '', fone)

def telefone_valido(fone: str) -> bool:
    fone_limpo = limpar_telefone(fone)
    return len(fone_limpo) in [10, 11]

def wrap_text(text, width=40):
    return '\n'.join(textwrap.wrap(str(text), width=width))

def ler_inteiro(min_val=None, max_val=None):
    while True:
        entrada = input()
        if entrada == '-1': return -1
        if entrada.isdigit():
            numero = int(entrada)
            if (min_val is None or numero >= min_val) and (max_val is None or numero <= max_val):
                return numero
            
            else:
                print(f"Digite um número entre {min_val} e {max_val}, ou digite '-1' para Sair.")

        else:
            print("Por favor, digite apenas números inteiros.")

def gerar_numero(digitos):
    menor = 10 ** (digitos - 1) if digitos > 1 else 0
    maior = 10 ** digitos - 1
    return random.randint(menor, maior)

def gerar_data_cert(ano=2025, mes=11):
    dia = random.randint(17, 30)
    return date(ano, mes, dia)

def gerar_data(codigo):
    inicio = atividades[codigo]["datainicio"]
    fim = atividades[codigo]["datafim"]
    dias = (fim - inicio).days
    data_aleatoria = inicio + timedelta(days=random.randint(0, dias))
    return data_aleatoria


def ler_cpf_valido():
    while True:
        cpf = input("\nCPF: ").strip()
        if cpf == '2': return '2'
        cpf = limpar_cpf(cpf)
        if cpf_valido(cpf): return cpf
        print("CPF inválido. Digite o CPF novamente ou digite '2' para Sair.")


def ler_data_atividade(codigo):
    data_inicio = atividades[codigo]["datainicio"]
    data_fim = atividades[codigo]["datafim"]
    while True:
        entrada = input("Data (DD/MM/AAAA): ").strip()
        if entrada == '2':
            return '2'
        try:
            data_formatada = datetime.strptime(entrada, "%d/%m/%Y").date()
            if (data_inicio <= data_formatada <= data_fim) or (data_formatada <= data_inicio <= data_fim):
                return data_formatada
            else:
                print(f"A data deve estar entre {data_inicio.strftime('%d/%m/%Y')} e {data_fim.strftime('%d/%m/%Y')}.")
        except ValueError:
            print("\nData inválida. Use o formato DD/MM/AAAA. Digite '2' para Sair.\n")

def ler_data_valida():
    while True:
        entrada = input("Data (DD/MM/AAAA): ").strip()
        if entrada == '2':
            return '2'
        try:
            data_formatada = datetime.strptime(entrada, "%d/%m/%Y").date()
            return data_formatada
        except ValueError:
            print("\nData inválida. Use o formato DD/MM/AAAA. Digite '2' para Sair.\n")

def ler_presenca_valida():
    while True:
        entrada = input("Participante esteve presente? (S/N): ").strip().lower()
        if entrada == '2': return '2'
        if entrada in ['s', 'sim']:
            return True
        elif entrada in ['n', 'nao', 'não', 'ñ']:
            return False
        else:
            print("\nEntrada inválida. Digite 'S' para SIM ou 'N' para NÃO, ou digite '2' para Sair.\n")

def ler_email_valido():
    while True:
        email = input("E-mail: ").lower().strip()
        if email == '2': return '2'
        if email_valido(email): return email
        print("\nE-mail inválido. Digite o e-mail novamente ou digite '2' para Sair.\n")


def ler_ocupacao_valida():
    while True:
        ocupacao = input("Ocupação (Aluno(a)/Visitante/Palestrante/Professor(a)): ").lower().strip()
        if ocupacao == '2': return '2'
        if ocupacao_valida(ocupacao): return ocupacao
        print("\nOcupação inválida. Digite a ocupação novamente ou digite '2' para Sair.\n")

def ler_nome_valido():
    while True:
        nome = input("Nome: ").strip()
        if nome == '2': return '2'
        if nome_valido(nome): return normalizar_nome(nome)
        print("\nNome inválido. Digite o nome novamente ou digite '2' para Sair.\n")

def ler_curso_valido():
    while True:
        try:
            cod = ler_inteiro(None, None)
            if cod == -1: return -1
            if cod in cursos:
                print(f"Curso selecionado: {cursos[cod]}")
                return cod
            else:
                print("Código inválido. Tente novamente ou digite '-1' para Sair.")
        except ValueError:
            print("Digite um número inteiro válido.")

def mostrar_atividade(codigo):
    atividade = atividades.get(codigo)

    if not atividade:
        print("Atividade não encontrada.")
        return

    nome = atividade["nome"]
    datainicio = atividade["datainicio"].strftime("%d/%m/%Y")
    datafim = atividade["datafim"].strftime("%d/%m/%Y")

    tabela = [[codigo, nome, datainicio, datafim]]
    cabecalho = ["Código", "Tema", "Início", "Fim"]
    
    print("\nAtividade selecionada:\n")
    print(tabulate(tabela, headers=cabecalho, tablefmt="rounded_grid"))

def ler_atividade_valida():
    while True:
        try:
            atividade = ler_inteiro(None, None)
            if atividade == -1: return -1
            if atividade in atividades:
                return atividade
            else:
                print("\nCódigo inválido. Tente novamente ou digite '-1' para Sair.\n")
        except ValueError:
            print("\nDigite um número inteiro válido.\n")

def ler_tipo_valido():
    while True:
        tipo_certificado = input("\nTipo de Certificado (Participação/Ministrante Evento/Ministrante Palestra): ").lower().strip()
        if tipo_certificado == '2': return '2'
        if tipo_valido(tipo_certificado): return normalizar_nome(tipo_certificado)
        print("\nTipo de certificado inválido. Digite o tipo novamente ou digite '2' para Sair.\n")

def ler_emissao_valida():
    while True:
        entrada = input("Certificado foi emitido? (S/N): ").strip().lower()
        if entrada == '2': return '2'
        if entrada in ['s', 'sim']:
            return True
        elif entrada in ['n', 'nao', 'não', 'ñ']:
            return False
        else:
            print("\nEntrada inválida. Digite 'S' para SIM ou 'N' para NÃO, ou digite '2' para Sair.\n")

def selecionar_arquivo():
    Tk().withdraw()
    return askopenfilename(title="\nSelecione uma imagem ou arquivo para o participante.\n")

def listar_atividades():
    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT a.Codigo, a.Tema, tp.Nome, a.Descricao, a.Programacao, a.DataInicio, a.DataFim, a.HorarioInicio, a.HorarioFim FROM Atividade AS a
                    LEFT JOIN TipoAtividade AS tp ON tp.Codigo = a.Cod_TipoAti""")
        atividades = cur.fetchall()

        print("\nAtividades:\n")
        cabecalho = ["Código", "Tema", "Tipo", "Descrição", "Programação", "Início", "Término", "Horário de Início", "Horário de Término"]

        dados_formatados = []
        for linha in atividades:
            linha_formatada = []
            for c in linha:
                if isinstance(c, str):
                    linha_formatada.append(wrap_text(c, 40))
                elif isinstance(c, time):
                    linha_formatada.append(c.strftime('%H:%M'))
                elif isinstance(c, date):
                    linha_formatada.append(c.strftime('%d/%m/%Y'))
                else:
                    linha_formatada.append(c)
            dados_formatados.append(linha_formatada)

        print(tabulate(dados_formatados, headers=cabecalho, tablefmt="rounded_grid"))

    finally:
        cur.close()
        conn.close()

def listar_cursos():
    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT c.Codigo, c.Nome, c.Tipo, d.Nome FROM Curso AS c
                    LEFT JOIN Departamento AS d ON d.Codigo = c.Cod_Departamento""")
        cursos = cur.fetchall()

        print("\nCursos:\n")
        cabecalho = ["Código", "Curso", "Tipo", "Departamento"]

        print(tabulate(cursos, headers=cabecalho, tablefmt="rounded_grid"))

    finally:
        cur.close()
        conn.close()