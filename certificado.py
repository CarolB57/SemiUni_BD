'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

from definicoes import *

def criar_certificado():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return

        cur.execute("SELECT CPF FROM Participante WHERE CPF = %s", (cpf,))
        cpf_participante = cur.fetchone()

        if not cpf_participante:
            print("\nParticipante não encontrado. Não foi possível criar um certificado.\n")
            return

        cur.execute("SELECT Ocupacao FROM Participante WHERE CPF = %s", (cpf,))
        ocupacao = cur.fetchone()[0].lower()

        cur.execute("SELECT Codigo, Presenca FROM Inscricao WHERE CPF_Participante = %s", (cpf,))
        inscricoes = cur.fetchall()

        if not inscricoes:
            print("\nNenhuma inscrição encontrada.\n")
            return

        for cod_inscricao, presenca in inscricoes:
            if not presenca:
                print(f"\nInscrição {cod_inscricao}: Presença não confirmada. Nenhum certificado gerado.\n")
                continue

            # Define tipo com base na ocupação
            if ocupacao in ['aluno', 'aluna', 'visitante']:
                tipo_certificado = 'Participação'

            elif ocupacao in ['professor', 'professora']:
                tipo_certificado = 'Ministrante Evento'

            elif ocupacao == 'palestrante':
                tipo_certificado = 'Ministrante Palestra'

            else:
                print(f"\nOcupação '{ocupacao}' não gera certificado automático.\n")
                continue
        
            emitido = True
            data_emissao = gerar_data_cert()

            codigos = []
            cur.execute("""SELECT Codigo FROM Certificado""")
            codigos = cur.fetchall()

            codigos = [c[0] for c in codigos]  # Extrai só os números

            cod_certificado = gerar_numero(7)
            while cod_certificado in codigos:
                cod_certificado = gerar_numero(7)

            # Verifica se já existe certificado para essa inscrição
            cur.execute("SELECT * FROM Certificado WHERE Cod_Inscricao = %s", (cod_inscricao,))
            cert = cur.fetchone()
            if cert:
                print(f"\nCertificado já existe para a inscrição {cod_inscricao}.\n")
                continue

            cur.execute("""INSERT INTO Certificado (Codigo, Cod_Inscricao, Tipo, Emitido, DataEmissao)
                            VALUES (%s, %s, %s, %s, %s)""", (cod_certificado, cod_inscricao, tipo_certificado, emitido, data_emissao))

            print(f"\nCertificado criado para a inscrição {cod_inscricao} ({tipo_certificado}).\n")
        
        conn.commit()
        return

    finally:
        cur.close()
        conn.close()

def listar_certificados():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\nEscolha uma opção a seguir: ")
        print("Digite '1' para Listar todos os certificados do sistema;")
        print("Digite '2' para Buscar um certificado;")
        print("Digite '3' para Sair.")
        resp = ler_inteiro(1, 3)

        if resp == 1:
            cur.execute("SELECT * FROM Certificado")
            if not cur.fetchall():
                print("\nNão há certificados registrados no sistema.\n")
                return

            cur.execute("""SELECT p.Nome, p.CPF, c.Codigo, c.Cod_Inscricao, c.Tipo, c.Emitido, c.DataEmissao
                            FROM Participante AS p
                            JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo""")
            certificados = cur.fetchall()

            print("\nCertificados:\n")
            cabecalho = ["Nome", "CPF", "Cod. Certificado", "Cod. Inscrição", "Tipo de Certificado", "Certificado Emitido?", "Data de Emissão do Certificado"]
            print(tabulate(certificados, headers=cabecalho, tablefmt="rounded_grid"))


        elif resp == 2:
            cpf = ler_cpf_valido()
            if cpf == '2': return

            cur.execute("SELECT * FROM Participante WHERE CPF = %s", (cpf,))
            cpf_participante = cur.fetchone()
            if not cpf_participante:
                print("\nParticipante não encontrado. Não foi possível fazer a busca.\n")
                return
            
            cur.execute("""SELECT * FROM Certificado AS c
                        JOIN Inscricao AS i ON c.Cod_Inscricao = i.Codigo
                        JOIN Participante AS p ON p.CPF = i.CPF_Participante
                        WHERE CPF = %s""", (cpf,))
            if not cur.fetchall():
                print("\nNão há certificados registrados para este participante.\n")
                return
            
            cur.execute("""SELECT p.Nome, p.CPF, c.Codigo, c.Cod_Inscricao, c.Tipo, c.Emitido, c.DataEmissao
                            FROM Participante AS p
                            JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo
                            WHERE p.CPF = %s""", (cpf,))
            
            certificados = cur.fetchall()
            
            print("\nCertificados:\n")
            cabecalho = ["Nome", "CPF", "Cod. Certificado", "Cod. Inscrição", "Tipo de Certificado", "Certificado Emitido?", "Data de Emissão do Certificado"]
            print(tabulate(certificados, headers=cabecalho, tablefmt="rounded_grid"))
                
        else: return

    finally:
        cur.close()
        conn.close()

def atualizar_certificado():
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
        

        cur.execute("""SELECT c.Codigo FROM Certificado AS c
                        LEFT JOIN Inscricao AS i ON c.Cod_Inscricao = i.Codigo
                        LEFT JOIN Participante AS p ON p.CPF = i.CPF_Participante
                        WHERE CPF = %s""", (cpf,))
        cod = cur.fetchall()
        codigos = [c[0] for c in cod]
        if not codigos:
            print("\nNenhum certificado encontrado para esse CPF.\n")
            return
        

        cur.execute("""SELECT p.Nome, p.CPF, c.Codigo, c.Cod_Inscricao, c.Tipo, c.Emitido, c.DataEmissao
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo
                            WHERE p.CPF = %s""", (cpf,))
            
        certificados = cur.fetchall()
            
        print("\nCertificados:\n")
        cabecalho = ["Nome", "CPF", "Cod. Certificado", "Cod. Inscrição", "Tipo de Certificado", "Certificado Emitido?", "Data de Emissão do Certificado"]
        print(tabulate(certificados, headers=cabecalho, tablefmt="rounded_grid"))


        if(len(codigos) > 1):
            while True:
                print("\nQual certificado deseja alterar?", end="")
                certificado_escolhido = ler_inteiro(1000000,  9999999) # O código tem 7 dígitos
                if certificado_escolhido == -1: return
                if certificado_escolhido not in codigos:
                    print("Digite um certificado válido.")
                else: 
                    cod_certificado = certificado_escolhido
                    break
        
        else: cod_certificado = codigos[0]

        novo_tipo = ler_tipo_valido()
        if novo_tipo == '2': return
        novo_emitido = ler_emissao_valida()
        if novo_emitido == '2': return
        if novo_emitido == False: nova_data = None
        else:
            nova_data = ler_data_valida()
            if nova_data == '2': return

        cur.execute("""UPDATE Certificado
                        SET Tipo = %s, Emitido = %s, DataEmissao = %s
                        WHERE Codigo = %s""", (novo_tipo, novo_emitido, nova_data, cod_certificado))
        conn.commit()
        print("\nCertificado atualizado com sucesso.\n")

        return

    finally:
        cur.close()
        conn.close()

def deletar_certificado():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("SELECT * FROM Participante WHERE CPF = %s", (cpf,))
        cpf_participante = cur.fetchone()
        
        if not cpf_participante:
            print("\nParticipante não encontrado. Não foi possível deletar o certificado.\n")
            return
        
        cur.execute("""SELECT c.Codigo FROM Certificado AS c
                        LEFT JOIN Inscricao AS i ON c.Cod_Inscricao = i.Codigo
                        LEFT JOIN Participante AS p ON p.CPF = i.CPF_Participante
                        WHERE CPF = %s""", (cpf,))
        cod = cur.fetchall()
        codigos = [c[0] for c in cod]  # Extrai só os números
        if not cod:
            print("\nNenhum certificado encontrado para esse CPF.\n")
            return
        
        cur.execute("""SELECT p.Nome, p.CPF, c.Codigo, c.Cod_Inscricao, c.Tipo, c.Emitido, c.DataEmissao
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo
                            WHERE p.CPF = %s""", (cpf,))
        certificados = cur.fetchall()
            
        print("\nCertificados:\n")
        cabecalho = ["Nome", "CPF", "Cod. Certificado", "Cod. Inscrição", "Tipo de Certificado", "Certificado Emitido?", "Data de Emissão do Certificado"]
        print(tabulate(certificados, headers=cabecalho, tablefmt="rounded_grid"))


        if len(codigos) == 1:
            print("\nDeseja realmente apagar o certificado do participante?")
            print("Digite '1' para Sim;")
            print("Digite '2' para Não.")
            resp = ler_inteiro(1, 2)

            if resp == 2:
                print("\nOperação cancelada.\n")
                return

            cur.execute("""DELETE FROM Certificado 
                            WHERE Cod_Inscricao IN (SELECT Codigo FROM Inscricao WHERE CPF_Participante = %s)""", (cpf,))
            conn.commit()

            print("\nCertificado deletado com sucesso.\n")
            return

        print("\nDeseja deletar apenas um certificado ou deletar todos os certificados?")
        print("Digite '1' para Deletar apenas um certificado;")
        print("Digite '2' para Deletar todos os certificados;")
        print("Digite '3' para Sair.")
        resp = ler_inteiro(1, 3)
        if resp == 3: return


        if resp == 1:
            while True:
                print("\nQual certificado deseja deletar? ", end="")
                certificado_escolhido = ler_inteiro(1000000,  9999999) # O código tem 7 dígitos
                if certificado_escolhido == -1: return
                if certificado_escolhido not in codigos:
                    print("\nDigite um certificado válido.\n")
                else: 
                    cod_certificado = certificado_escolhido
                    break

            print("\nDeseja realmente apagar o certificado selecionado?")
            print("Digite '1' para Sim;")
            print("Digite '2' para Não.")
            resp2 = ler_inteiro(1, 2)
            if resp2 == 2: return

            
            cur.execute("""DELETE FROM Certificado 
                            WHERE (Codigo = %s) AND Cod_Inscricao IN (SELECT Codigo FROM Inscricao WHERE CPF_Participante = %s)""", (cod_certificado, cpf))
            conn.commit()

            print("\nCertificado deletado com sucesso.\n")
            return
        
        
        print("\nDeseja realmente apagar todos os certificados relacionados ao participante?")
        print("Digite '1' para Sim;")
        print("Digite '2' para Não.")
        resp = ler_inteiro(1, 2)

        if resp == 2:
            print("\nOperação cancelada.\n")
            return

        cur.execute("""DELETE FROM Certificado 
                        WHERE Cod_Inscricao IN (SELECT Codigo FROM Inscricao WHERE CPF_Participante = %s)""", (cpf,))
        conn.commit()

        print("\nCertificados deletados com sucesso.\n")

    finally:
        cur.close()
        conn.close()