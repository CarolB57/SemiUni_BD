'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

from definicoes import *

def criar_participante():
    conn = conectar()
    cur = conn.cursor()

    print("\nDigite os seguintes dados do participante:")
    cpf = ler_cpf_valido()
    if cpf == '2': return
    nome = ler_nome_valido()
    if nome == '2': return
    email = ler_email_valido()
    if email == '2': return
    ocupacao = ler_ocupacao_valida()
    if ocupacao == '2': return

    if ocupacao not in ['visitante', 'palestrante']:
        print("Código do curso: ", end="")
        cod_curso = ler_curso_valido()
        if cod_curso == -1: return
    else: cod_curso = None

    print("Telefone(s): Quantos telefones deseja inserir? (Digite um número) ", end="")
    num_tel = ler_inteiro(0, 4)
    if num_tel != 0: print("Digite os telefones: ")

    telefones = []
    i = 0
    while i < num_tel:
        tel = input(f"Telefone {i+1}: ")
        if telefone_valido(tel):
            telefone = limpar_telefone(tel)
            telefones.append(telefone)
            i += 1
        else: print("Digite um telefone válido!")


    try:
        cur.execute("""INSERT INTO Participante (CPF, Nome, Ocupacao, Email, Cod_curso)
                       VALUES (%s, %s, %s, %s, %s)""", (cpf, nome, ocupacao.capitalize(), email, cod_curso))
        
        for telefone in telefones:
            cur.execute("""INSERT INTO Telefone (CPF_participante, Fone)
                        VALUES (%s, %s)""", (cpf, telefone))
        conn.commit()
        print("\nParticipante criado com sucesso.\n")
    
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("\nErro: este CPF já existe no cadastro. Nenhum participante foi inserido.\n")

    except Exception as e:
        conn.rollback()
        print(f"\nErro inesperado: {e}\n")

    finally:
        cur.close()
        conn.close()

def listar_participantes():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\nEscolha uma opção a seguir: ")
        print("Digite '1' para Listar todos os participantes do sistema;")
        print("Digite '2' para Buscar um participante;")
        print("Digite '3' para Sair.")
        resp = ler_inteiro(1, 3)

        if resp == 1:
            print("\nGostaria de imprimir todos os dados relacionadas aos participantes? ")
            print("Digite '1' para Sim;")
            print("Digite '2' para Não;")
            print("Digite '3' para Sair.")
            resp2 = ler_inteiro(1, 3)
            if resp2 == 3: return

            
            cur.execute("SELECT * FROM Participante")
            participantes = cur.fetchall()

            if not participantes:
                print("\nNenhum participante encontrado.\n")
                return

            cur.execute("""SELECT p.Nome, p.CPF, p.Ocupacao, p.Email, p.Cod_Curso, c.Nome, d.Nome, p.FotoCadastrada
                            FROM Participante AS p
                            LEFT JOIN Curso AS c ON c.Codigo = p.Cod_Curso
                            LEFT JOIN Departamento AS d ON d.Codigo = c.Cod_Departamento""")
            dados = cur.fetchall()
                    
            print("\nParticipantes:\n")
            cabecalho = ["Nome", "CPF", "Ocupação", "E-mail", "Cod. Curso", "Curso", "Departamento", "Foto foi Cadastrada?"]
            print(tabulate(dados, headers=cabecalho, tablefmt="rounded_grid"))


            telefones = []
            cur.execute("""SELECT p.Nome, t.Fone
                            FROM Participante AS p
                            LEFT JOIN Telefone AS t ON t.CPF_participante = p.CPF""")
            telefones = cur.fetchall()

            if telefones:
                cabecalho = ["Nome", "Telefone"]
                print(tabulate(telefones, headers=cabecalho, tablefmt="rounded_grid"))
            else: 
                print("Nenhum telefone encontrado.")
            
            if resp2 == 2: return

            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, i.Codigo, i.DataInscricao, i.Presenca
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade""")
            dados2 = cur.fetchall()

            if dados2:
                print("\nInscrições:\n")
                cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Cod. Inscrição", "Data de Inscrição", "Presença"]
                print(tabulate(dados2, headers=cabecalho, tablefmt="rounded_grid"))
            else:
                print("\nNenhuma inscrição encontrada.\n")


            cur.execute("""SELECT p.Nome, p.CPF, c.Codigo, c.Cod_Inscricao, c.Tipo, c.Emitido, c.DataEmissao, f.Nota, f.Comentario
                            FROM Participante AS p
                            JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo
                            LEFT JOIN Feedback AS f ON f.Cod_Inscricao = c.Cod_Inscricao""")
            dados3 = cur.fetchall()

            if dados3:
                print("\nCertificados e Feedbacks:\n")
                cabecalho = ["Nome", "CPF", "Cod. Certificado", "Cod. Inscrição", "Tipo de Certificado", "Certificado Emitido?", 
                            "Data de Emissão do Certificado", "Nota Feedback", "Comentário"]

                dados_formatados = []
                for linha in dados3:
                    linha_formatada = [wrap_text(c, 40) if isinstance(c, str) else c for c in linha]
                    dados_formatados.append(linha_formatada)

                print(tabulate(dados_formatados, headers=cabecalho, tablefmt="rounded_grid"))

            else:
                print("\nNenhum certificado/feedback encontrado.\n")


        elif resp == 2:
            cpf = ler_cpf_valido()
            if cpf == '2': return

            cur.execute("SELECT * FROM Participante WHERE CPF = %s", (cpf,))
            participante = cur.fetchone()
            if not participante:
                print("Participante não encontrado.")
                return
            
            cur.execute("SELECT Nome FROM Participante WHERE CPF = %s", (cpf,))
            n = cur.fetchone()
            nome = n[0]
            
            print(f"\nGostaria de imprimir todos os dados relacionados a {nome}?")
            print("Digite '1' para Sim;")
            print("Digite '2' para Não;")
            print("Digite '3' para Sair.")
            resp2 = ler_inteiro(1, 3)
            if resp2 == 3: return


            cur.execute("""SELECT p.Nome, p.CPF, p.Ocupacao, p.Email, p.Cod_Curso, c.Nome, d.Nome, p.FotoCadastrada
                            FROM Participante AS p
                            LEFT JOIN Curso AS c ON c.Codigo = p.Cod_Curso
                            LEFT JOIN Departamento AS d ON d.Codigo = c.Cod_Departamento
                            WHERE p.CPF = %s""", (cpf,))
            dados = cur.fetchone()
                    
            print("\nParticipante:\n")
            cabecalho = ["Nome", "CPF", "Ocupação", "E-mail", "Cod. Curso", "Curso", "Departamento", "Foto foi Cadastrada?"]
            print(tabulate([dados], headers=cabecalho, tablefmt="rounded_grid"))


            telefones = []
            cur.execute("""SELECT p.Nome, t.Fone
                            FROM Participante AS p
                            LEFT JOIN Telefone AS t ON t.CPF_participante = p.CPF
                            WHERE p.CPF = %s""", (cpf,))
            telefones = cur.fetchall()

            if telefones:
                cabecalho = ["Nome", "Telefone"]
                print(tabulate(telefones, headers=cabecalho, tablefmt="rounded_grid"))
            else: 
                print("Nenhum telefone encontrado.")

            if resp2 == 2: return

            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, i.Codigo, i.DataInscricao, i.Presenca
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade
                            WHERE p.CPF = %s""", (cpf,))
            dados2 = cur.fetchall()

            if dados2:
                    print("\nInscrições:\n")
                    cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Cod. Inscrição", "Data de Inscrição", "Presença"]
                    print(tabulate(dados2, headers=cabecalho, tablefmt="rounded_grid"))
            else:
                print("Nenhuma inscrição encontrada.")


            cur.execute("""SELECT p.Nome, p.CPF, c.Codigo, c.Cod_Inscricao, c.Tipo, c.Emitido, c.DataEmissao, f.Nota, f.Comentario
                            FROM Participante AS p
                            JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            JOIN Certificado AS c ON c.Cod_Inscricao = i.Codigo
                            LEFT JOIN Feedback AS f ON f.Cod_Inscricao = c.Cod_Inscricao
                            WHERE p.CPF = %s""", (cpf,))
            dados3 = cur.fetchall()

            if dados3:
                print("\nCertificados e Feedbacks:\n")
                cabecalho = ["Nome", "CPF", "Cod. Certificado", "Cod. Inscrição", "Tipo de Certificado", "Certificado Emitido?", 
                                "Data de Emissão do Certificado", "Nota Feedback", "Comentário"]

                dados_formatados = []
                for linha in dados3:
                    linha_formatada = [wrap_text(c, 40) if isinstance(c, str) else c for c in linha]
                    dados_formatados.append(linha_formatada)

                print(tabulate(dados_formatados, headers=cabecalho, tablefmt="rounded_grid"))

            else:
                print("\nNenhum certificado/feedback encontrado.\n")

                
        else: return

    finally:
        cur.close()
        conn.close()

def atualizar_participante():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("""SELECT * FROM Participante WHERE CPF = %s""", (cpf,))
        participante = cur.fetchone()

        cur.execute("""SELECT Ocupacao FROM Participante WHERE CPF = %s""", (cpf,))
        ocupacao = cur.fetchone()

        telefones = []
        cur.execute("""SELECT p.Nome, t.Fone
                        FROM Participante AS p
                        LEFT JOIN Telefone AS t ON t.CPF_participante = p.CPF
                        WHERE p.CPF = %s""", (cpf,))
        telefones = cur.fetchall()

        if not participante:
            print("\nParticipante não encontrado.\n")
            return
        
        cur.execute("""SELECT p.Nome, p.CPF, p.Ocupacao, p.Email, p.Cod_Curso, c.Nome, d.Nome, p.FotoCadastrada
                        FROM Participante AS p
                        LEFT JOIN Curso AS c ON c.Codigo = p.Cod_Curso
                        LEFT JOIN Departamento AS d ON d.Codigo = c.Cod_Departamento
                        WHERE p.CPF = %s""", (cpf,))
        dados = cur.fetchall()
                    
        print("\nDados atuais:\n")
        cabecalho = ["Nome", "CPF", "Ocupação", "E-mail", "Cod. Curso", "Curso", "Departamento", "Foto foi Cadastrada?"]
        print(tabulate(dados, headers=cabecalho, tablefmt="rounded_grid"))
        
        if telefones:
            print("\nTelefones atuais:\n")
            cabecalho = ["Nome", "Telefone"]
            print(tabulate(telefones, headers=cabecalho, tablefmt="rounded_grid"))
        else: 
            print("Nenhum telefone encontrado.")
        

        print("\nDeseja alterar todos os dados?")
        print("Digite '1' para Sim;")
        print("Digite '2' para Não;")
        print("Digite '3' para Sair.")
        resp = ler_inteiro(1, 3)

        if resp == 1:
            novo_nome = ler_nome_valido()
            if novo_nome == '2': return
            novo_email = ler_email_valido()
            if novo_email == '2': return
            nova_ocupacao = ler_ocupacao_valida()
            if nova_ocupacao == '2': return

            if nova_ocupacao not in ['visitante', 'palestrante']:
                print("Código do curso: ", end="")
                novo_cod_curso = ler_curso_valido()
                if novo_cod_curso == -1: return
            else: novo_cod_curso = None
            
            print("Telefone(s): Quantos telefones deseja inserir? (Digite um número) ", end="")
            num_tel = ler_inteiro(0, 4)
            if num_tel != 0: print("Digite os telefones: ")

            novos_telefones = []
            i = 0
            while i < num_tel:
                tel = input(f"Telefone {i+1}: ")
                if telefone_valido(tel):
                    novo_telefone = limpar_telefone(tel)
                    novos_telefones.append(novo_telefone)
                    i += 1
                else: print("Digite um telefone válido!")


            cur.execute("DELETE FROM Telefone WHERE CPF_participante = %s", (cpf,))

            cur.execute("""UPDATE Participante
                        SET Nome = %s, Email = %s, Ocupacao = %s, Cod_Curso = %s
                        WHERE CPF = %s""", (novo_nome, novo_email, nova_ocupacao.capitalize(), novo_cod_curso if novo_cod_curso else None, cpf))
            
            for novo_telefone in novos_telefones:
                cur.execute("""INSERT INTO Telefone (CPF_participante, Fone) VALUES (%s, %s)""", (cpf, novo_telefone))
            
            conn.commit()
            print("\nParticipante atualizado com sucesso.\n")

            return


        elif resp == 2:
            print("\nQual dado deseja alterar?")
            print("Digite '1' para Nome;")
            print("Digite '2' para Email;")
            print("Digite '3' para Ocupação;")
            print("Digite '4' para Código do Curso;")
            print("Digite '5' para Telefones;")
            print("Digite '6' para Voltar.")
            resp2 = ler_inteiro(1, 6)

            if resp2 == 1:
                novo_nome = ler_nome_valido()
                cur.execute("""UPDATE Participante
                            SET Nome = %s WHERE CPF = %s""", (novo_nome, cpf))
                conn.commit()
                print("\nNome atualizado com sucesso.\n")
                return
            
            elif resp2 == 2:
                novo_email = ler_email_valido()
                
                cur.execute("""UPDATE Participante
                            SET Email = %s WHERE CPF = %s""", (novo_email, cpf))
                
                conn.commit()
                print("\nE-mail atualizado com sucesso.\n")
                return
            
            elif resp2 == 3:
                nova_ocupacao = ler_ocupacao_valida()
                
                cur.execute("""SELECT Cod_Curso FROM Participante WHERE CPF = %s""", (cpf,))
                codigo = cur.fetchone()
                cod_curso = codigo[0] if codigo else None

                if nova_ocupacao in ['visitante', 'palestrante']: cod_curso = None
                
                
                cur.execute("""UPDATE Participante
                            SET Ocupacao = %s, Cod_Curso = %s WHERE CPF = %s""", (nova_ocupacao.capitalize(), cod_curso, cpf))
                
                
                conn.commit()
                print("\nOcupação atualizada com sucesso.\n")
                return
            
            elif resp2 == 4 and ocupacao not in ['visitante', 'palestrante']:
                print("Código do curso: ", end="")
                novo_cod_curso = ler_curso_valido()
                if novo_cod_curso == -1: return

                cur.execute("""UPDATE Participante
                            SET Cod_curso = %s WHERE CPF = %s""", (novo_cod_curso, cpf))
                
                conn.commit()
                print("\nCódigo do curso atualizado com sucesso.\n")
                return
            
            elif resp2 == 4 and ocupacao in ['visitante', 'palestrante']: 
                print("\nO participante não pode mudar o código do curso, uma vez que não é associado à UnB.\n")
                return
            
            elif resp2 == 5:
                print("Quantos telefones deseja inserir? (Digite um número)")
                num_tel = ler_inteiro(0, 4)
                if num_tel != 0: print("Digite os telefones: ")
                
                novos_telefones = []
                i = 0
                while i < num_tel:
                    tel = input(f"Telefone {i+1}: ")
                    if telefone_valido(tel):
                        novo_telefone = limpar_telefone(tel)
                        novos_telefones.append(novo_telefone)
                        i += 1
                    else: print("Digite um telefone válido!")
                

                cur.execute("DELETE FROM Telefone WHERE CPF_participante = %s", (cpf,))

                for novo_telefone in novos_telefones:
                    cur.execute("""INSERT INTO Telefone (CPF_participante, Fone) VALUES (%s, %s)""", (cpf, novo_telefone))
                
                conn.commit()
                print("\nTelefone(s) atualizado(s) com sucesso.\n")
                return
            
            else: return
        else: return

    finally:
        cur.close()
        conn.close()

def deletar_participante():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("SELECT * FROM Participante WHERE CPF = %s", (cpf,))
        participante = cur.fetchone()
        
        if not participante:
            print("Participante não encontrado.")
            return

        # Coleta dados relacionados
        cur.execute("SELECT Codigo FROM Inscricao WHERE CPF_Participante = %s", (cpf,))
        inscricao = cur.fetchall()
        codigos = [i[0] for i in inscricao]

        cur.execute("SELECT * FROM Telefone WHERE CPF_participante = %s", (cpf,))
        telefones = cur.fetchall()

        certificados = []
        feedbacks = []

        if codigos:
            placeholders = ','.join(['%s'] * len(codigos))
            cur.execute(f"SELECT * FROM Certificado WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))
            certificados = cur.fetchall()

            cur.execute(f"SELECT * FROM Feedback WHERE Cod_Inscricao IN ({placeholders})", tuple(codigos))
            feedbacks = cur.fetchall()

        cur.execute("""SELECT p.Nome, p.CPF, p.Ocupacao, p.Email, p.Cod_Curso, c.Nome, d.Nome, p.FotoCadastrada
                        FROM Participante AS p
                        LEFT JOIN Curso AS c ON c.Codigo = p.Cod_Curso
                        LEFT JOIN Departamento AS d ON d.Codigo = c.Cod_Departamento
                        WHERE p.CPF = %s""", (cpf,))
        dados = cur.fetchone()
        print("\nParticipante:\n")
        cabecalho = ["Nome", "CPF", "Ocupação", "E-mail", "Cod. Curso", "Curso", "Departamento", "Foto foi Cadastrada?"]
        print(tabulate([dados], headers=cabecalho, tablefmt="rounded_grid"))

        print(f"\nDados relacionados a este participante:\n")

        print(f"\n{len(inscricao)} inscrição(ões):\n")
        if inscricao:
            cur.execute("""SELECT p.Nome, p.CPF, a.Codigo, a.Tema, i.Codigo, i.DataInscricao, i.Presenca
                            FROM Participante AS p
                            LEFT JOIN Inscricao AS i ON p.CPF = i.CPF_Participante
                            LEFT JOIN Atividade AS a ON a.Codigo = i.Cod_Atividade
                            WHERE p.CPF = %s""", (cpf,))
            insc = cur.fetchall()

            cabecalho = ["Nome", "CPF", "Cod. Atividade", "Tema da Atividade", "Cod. Inscrição", "Data de Inscrição", "Esteve presente?"]
            print(tabulate(insc, headers=cabecalho, tablefmt="rounded_grid"))



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


        print(f"\n{len(telefones)} telefone(s)\n")
        if telefones:
            cur.execute("""SELECT p.Nome, t.Fone
                            FROM Participante AS p
                            LEFT JOIN Telefone AS t ON p.CPF = t.CPF_participante
                            WHERE p.CPF = %s""", (cpf,))
            tel = cur.fetchall()
            cabecalho = ["Nome", "Telefone"]
            print(tabulate(tel, headers=cabecalho, tablefmt="rounded_grid"))


        print("\nDeseja realmente apagar todos esses dados e o participante?")
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
        if inscricao:
            cur.execute("DELETE FROM Inscricao WHERE CPF_Participante = %s", (cpf,))
        if telefones:
            cur.execute("DELETE FROM Telefone WHERE CPF_participante = %s", (cpf,))

        # Sempre deletar participante no final
        cur.execute("DELETE FROM Participante WHERE CPF = %s", (cpf,))
        conn.commit()

        print("\nParticipante e dados relacionados deletados com sucesso.\n")

    finally:
        cur.close()
        conn.close()