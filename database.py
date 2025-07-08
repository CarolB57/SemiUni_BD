'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="SemiUni",
        user="postgres",
        password="1", 
        host="localhost",
        port="5432"
    )