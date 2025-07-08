'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

from definicoes import *

def criar_inscricao():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return

        cur.execute("""SELECT CPF FROM Participante WHERE CPF = %s""", (cpf,))
        cpf_participante = cur.fetchone()

        if not cpf_participante:
            print("Participante não encontrado. Não foi possível criar uma inscrição.")
            return
        
        print("Código do atividade: ", end="")
        cod_atividade = ler_atividade_valida()
        if cod_atividade == -1: return

        cur.execute("""SELECT 1 FROM Inscricao
                        WHERE CPF_Participante = %s AND Cod_Atividade = %s""", (cpf, cod_atividade))
        participacao = cur.fetchone()

        if participacao:
            print("\nParticipante já está inscrito nessa atividade.\n")
            return
        
        cur.execute("""SELECT COUNT(*) FROM Inscricao
                        WHERE Cod_Atividade = %s""", (cod_atividade,))
        qntd = cur.fetchone()[0]

        cur.execute("""SELECT Vagas FROM Atividade
                        WHERE Codigo = %s""", (cod_atividade,))
        vagas = cur.fetchone()[0]

        if qntd >= vagas:
            print("\nNão há mais vagas para essa adividade.\n")
            return
        
        mostrar_atividade(cod_atividade)

        data = gerar_data(cod_atividade)
        presenca = False  # padrão: ainda não registrado

        codigos = []
        cur.execute("""SELECT Codigo FROM Inscricao""")
        codigos = cur.fetchall()

        codigos = [c[0] for c in codigos]  # Extrai só os números

        cod_incricao = gerar_numero(8)
        while cod_incricao in codigos:
            cod_incricao = gerar_numero(8)

        if cod_incricao is not None:
            cur.execute("""INSERT INTO Inscricao (Codigo, Cod_Atividade, CPF_Participante, DataInscricao, Presenca)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (cod_incricao, cod_atividade, cpf, data, presenca))
            
            conn.commit()
            print("\nInscrição criada com sucesso.\n")
        else: print("\nNão foi possível criar a inscrição.\n")
        return

    finally:
        cur.close()
        conn.close()

def listar_inscricoes():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\nEscolha uma opção a seguir: ")
        print("Digite '1' para Listar todas as inscrições do sistema;")
        print("Digite '2' para Buscar uma inscrição;")
        print("Digite '3' para Sair.")
        resp = ler_inteiro(1, 3)

        if resp == 1:
            cur.execute("SELECT * FROM Inscricao")
            if not cur.fetchall():
                print("Não há inscrições registradas no sistema.")
                return

            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, i.Codigo, i.DataInscricao, i.Presenca
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade""")
            inscricoes = cur.fetchall()

            print("\nInscrições:\n")
            cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Cod. Inscrição", "Data de Inscrição", "Esteve presente?"]
            print(tabulate(inscricoes, headers=cabecalho, tablefmt="rounded_grid"))

        elif resp == 2:
            cpf = ler_cpf_valido()
            if cpf == '2': return

            cur.execute("SELECT * FROM Participante WHERE CPF = %s", (cpf,))
            cpf_participante = cur.fetchone()
            if not cpf_participante:
                print("Participante não encontrado. Não foi possível fazer a busca.")
                return
            
            cur.execute("SELECT * FROM Inscricao WHERE CPF = %s", (cpf,))
            if not cur.fetchall():
                print("\nNão há inscrições registradas para este participante.\n")
                return
            
            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, i.Codigo, i.DataInscricao, i.Presenca
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade
                            WHERE p.CPF = %s""", (cpf,))
            tabela = cur.fetchall()
            
            print("\nInscrições:\n")
            cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Cod. Inscrição", "Data de Inscrição", "Presença"]
            print(tabulate(tabela, headers=cabecalho, tablefmt="rounded_grid"))
                
        else:
            return

    finally:
        cur.close()
        conn.close()
    
def atualizar_inscricao():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("""SELECT * FROM Participante WHERE CPF = %s""", (cpf,))
        cpf_participante = cur.fetchone()

        if not cpf_participante:
            print("\nParticipante não encontrado. Não foi possível alterar a inscrição.\n")
            return


        cur.execute("""SELECT Codigo FROM Inscricao WHERE CPF_Participante = %s""", (cpf,))
        cod = cur.fetchall()

        codigos = [c[0] for c in cod]  # Extrai só os números

        if not codigos:
            print("\nNenhuma inscrição encontrada para esse CPF.\n")
            return


        print("\nInscrições:\n")
        cur.execute("""SELECT i.Codigo, p.Nome, p.CPF, a.Tema, i.DataInscricao, i.Presenca
                    FROM Participante AS p
                    LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                    LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade
                    WHERE p.CPF = %s""", (cpf,))
        tabela = cur.fetchall()
        cabecalho = ["Cod. Inscrição", "Nome", "CPF", "Tema da Atividade", "Data de Inscrição", "Presença"]
        print(tabulate(tabela, headers=cabecalho, tablefmt="rounded_grid"))

 
        if(len(codigos) > 1):
            while True:
                print("\nQual inscrição deseja alterar? ", end="")
                inscricao_escolhida = ler_inteiro(10000000, 99999999) # O código tem 8 dígitos
                if inscricao_escolhida == -1: return
                if inscricao_escolhida not in codigos:
                    print("\nDigite uma inscrição válida.\n")
                else: 
                    cod_inscricao = inscricao_escolhida
                    break
        
        else: cod_inscricao = codigos[0]

        cur.execute("""SELECT Cod_Atividade FROM Inscricao WHERE Codigo = %s""", (cod_inscricao,))
        codigo = cur.fetchone()
        if not codigo:
            print("\nCódigo da atividade não encontrado.\n")
            return
        cod_atividade = codigo[0]

        nova_data = ler_data_atividade(cod_atividade)
        if nova_data == '2': return
        nova_presenca = ler_presenca_valida()
        if nova_presenca == '2': return

        cur.execute("""UPDATE Inscricao
                        SET DataInscricao = %s, Presenca = %s
                        WHERE Codigo = %s""", (nova_data, nova_presenca, cod_inscricao))
        conn.commit()
        print("\nInscrição atualizada com sucesso.\n")

        if nova_presenca == False:
            cur.execute("""SELECT * FROM Certificado WHERE Cod_Inscricao = %s""", (cod_inscricao,))
            cert = cur.fetchone()

            if cert:
                cur.execute("""DELETE FROM Certificado WHERE Cod_Inscricao = %s""", (cod_inscricao,))
                conn.commit()
                print(f"\nCertificado da inscrição {cod_inscricao} removido devido à ausência.\n")

        return

    finally:
        cur.close()
        conn.close()

# APAGAR TODAS AS INSCRIÇÕES OU APENAS UMA!!!
def deletar_inscricao():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("SELECT * FROM Participante WHERE CPF = %s", (cpf,))
        cpf_participante = cur.fetchone()
        
        if not cpf_participante:
            print("\nParticipante não encontrado. Não foi possível deletar a inscrição.\n")
            return
        
        cur.execute("""SELECT Codigo FROM Inscricao WHERE CPF_Participante = %s""", (cpf,))
        cod = cur.fetchall()

        codigos = [c[0] for c in cod]  # Extrai só os números

        if not codigos:
            print("\nNenhuma inscrição encontrada para esse CPF.\n")
            return


        print("\nInscrições:\n")
        cur.execute("""SELECT i.Codigo, p.Nome, p.CPF, a.Codigo, a.Tema, i.DataInscricao, i.Presenca
                    FROM Participante AS p
                    LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                    LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade
                    WHERE p.CPF = %s""", (cpf,))
        tabela = cur.fetchall()
        cabecalho = ["Cod. Inscrição", "Nome", "CPF", "Cod. da Atividade", "Tema da Atividade", "Data de Inscrição", "Presença"]
        print(tabulate(tabela, headers=cabecalho, tablefmt="rounded_grid"))


        certificados = []
        feedbacks = []

        if codigos:
            placeholders = ','.join(['%s'] * len(codigos))
            cur.execute(f"SELECT * FROM Certificado WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))
            certificados = cur.fetchall()

            cur.execute(f"SELECT * FROM Feedback WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))
            feedbacks = cur.fetchall()

        print(f"\nDados relacionados a este participante:")
        print(f"\n{len(certificados)} certificado(s)\n")
        if certificados:
            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, c.Codigo, c.Tipo, c.Emitido, c.DataEmissao
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade
                            LEFT JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo
                            WHERE p.CPF = %s""", (cpf,))
            cert = cur.fetchall()
            cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Cod. Certificado", "Tipo de Certificado",  "Certificado foi emitido?", 
                         "Data de Emissão do Certificado"]
            print(tabulate(cert, headers=cabecalho, tablefmt="rounded_grid"))


        print(f"\n{len(feedbacks)} feedback(s)\n")
        if feedbacks:
            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, f.Nota, f.Comentario
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON i.Cod_Atividade = a.Codigo
                            LEFT JOIN Feedback AS f ON f.Cod_Inscricao = i.Codigo
                            WHERE p.CPF = %s""", (cpf,))
            feed = cur.fetchall()

            cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Nota Feedback", "Comentário"]

            dados_formatados = []
            for linha in feed:
                linha_formatada = [wrap_text(c, 40) if isinstance(c, str) else c for c in linha]
                dados_formatados.append(linha_formatada)

            print(tabulate(dados_formatados, headers=cabecalho, tablefmt="rounded_grid"))
        
        if len(codigos) == 1:
            print("\nDeseja realmente apagar todos esses dados e a inscrição do participante?")
            print("Digite '1' para Sim;")
            print("Digite '2' para Não.")
            resp = ler_inteiro(1, 2)

            if resp == 2:
                print("\nOperação cancelada.\n")
                return

            # Deleção apenas se existir
            if feedbacks:
                cur.execute(f"DELETE FROM Feedback WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))
            if certificados:
                cur.execute(f"DELETE FROM Certificado WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))

            cur.execute("DELETE FROM Inscricao WHERE CPF_Participante = %s", (cpf,))
            conn.commit()

            print("\nInscrição e dados relacionados deletados com sucesso.\n")
            return
                

        print("\nDeseja deletar apenas uma inscrição ou deletar todas as inscrições?")
        print("Digite '1' para Deletar apenas uma inscrição;")
        print("Digite '2' para Deletar todas as inscrições;")
        print("Digite '3' para Sair.")
        resp = ler_inteiro(1, 3)
        if resp == 3: return


        if resp == 1:
            while True:
                print("\nQual inscrição deseja deletar? ", end="")
                inscricao_escolhida = ler_inteiro(10000000, 99999999) # O código tem 8 dígitos
                if inscricao_escolhida == -1: return
                if inscricao_escolhida not in codigos:
                    print("Digite uma inscrição válida.")
                else: 
                    cod_inscricao = inscricao_escolhida
                    break

            print("\nDeseja realmente apagar todos esses dados e a inscrição do participante?")
            print("Digite '1' para Sim;")
            print("Digite '2' para Não.")
            resp2 = ler_inteiro(1, 2)
            if resp2 == 2: return

            if feedbacks:
                cur.execute("DELETE FROM Feedback WHERE Cod_Inscricao = %s", (cod_inscricao,))
            if certificados:
                cur.execute("DELETE FROM Certificado WHERE Cod_Inscricao = %s", (cod_inscricao,))

            cur.execute("DELETE FROM Inscricao WHERE CPF_Participante = %s AND Codigo = %s", (cpf, cod_inscricao))
            conn.commit()

            print("\nInscrição e dados relacionados deletados com sucesso.\n")
            return
            

        print("\nDeseja realmente apagar todos esses dados e a inscrição do participante?")
        print("Digite '1' para Sim;")
        print("Digite '2' para Não.")
        resp = ler_inteiro(1, 2)

        if resp == 2:
            print("\nOperação cancelada.\n")
            return

        # Deleção apenas se existir
        if feedbacks:
            cur.execute(f"DELETE FROM Feedback WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))
        if certificados:
            cur.execute(f"DELETE FROM Certificado WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))

        cur.execute("DELETE FROM Inscricao WHERE CPF_Participante = %s", (cpf,))
        conn.commit()

        print("\nInscrição e dados relacionados deletados com sucesso.\n")

    finally:
        cur.close()
        conn.close()