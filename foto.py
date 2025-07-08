'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

from definicoes import *

def inserir_foto():
    conn = conectar()
    cur = conn.cursor()
    
    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("SELECT 1 FROM Participante WHERE CPF = %s", (cpf,))
        if not cur.fetchone():
            print("\nParticipante não encontrado.\n")
            return

        cur.execute("SELECT Foto FROM Participante WHERE CPF = %s", (cpf,))
        foto_existente = cur.fetchone()[0]
        if foto_existente:
            print("\nEsse participante já possui uma foto cadastrada.\n")
            return

        caminho_arquivo = selecionar_arquivo()
        if not caminho_arquivo:
            print("\nNenhum arquivo selecionado.\n")
            return

        with open(caminho_arquivo, "rb") as f:
            conteudo_binario = f.read()

        cur.execute("UPDATE Participante SET Foto = %s WHERE CPF = %s", (Binary(conteudo_binario), cpf))
        cur.execute("UPDATE Participante SET FotoCadastrada = TRUE WHERE CPF = %s", (cpf,))
        conn.commit()
        print("\nArquivo inserido com sucesso no banco de dados.\n")

    except Exception as e:
        print("\nErro ao inserir o arquivo:", e)

    finally:
        cur.close()
        conn.close()

def salvar_foto():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("SELECT 1 FROM Participante WHERE CPF = %s", (cpf,))
        if not cur.fetchone():
            print("\nParticipante não encontrado.\n")
            return
        
        cur.execute("SELECT Foto FROM Participante WHERE CPF = %s", (cpf,))
        resultado = cur.fetchone()

        if resultado and resultado[0]:
            # Inicia uma janela oculta do tkinter
            root = tk.Tk()
            root.withdraw()

            # Abre janela para escolher onde salvar
            caminho = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Salvar imagem"
            )

            if caminho:
                with open(caminho, "wb") as f:
                    f.write(resultado[0])
                print(f"Foto salva em: {caminho}")
            else:
                print("\nOperação cancelada pelo usuário.\n")
        else:
            print("\nNenhuma foto encontrada para esse CPF.\n")
    finally:
        cur.close()
        conn.close()

def deletar_foto():
    conn = conectar()
    cur = conn.cursor()

    try:
        cpf = ler_cpf_valido()
        if cpf == '2': return
        cur.execute("SELECT 1 FROM Participante WHERE CPF = %s", (cpf,))
        if not cur.fetchone():
            print("\nParticipante não encontrado.\n")
            return

        cur.execute("SELECT Foto FROM Participante WHERE CPF = %s", (cpf,))
        foto = cur.fetchone()

        if not foto or not foto[0]:
            print("\nNenhuma foto encontrada para esse participante.\n")
            return

        print("\nDeseja realmente apagar a foto do participante em questão?")
        print("Digite '1' para Sim;")
        print("Digite '2' para Não.")
        resp = ler_inteiro(1, 2)

        if resp == 2:
            print("\nOperação cancelada.\n")
            return

        cur.execute("UPDATE Participante SET Foto = NULL WHERE CPF = %s", (cpf,))
        cur.execute("UPDATE Participante SET FotoCadastrada = FALSE WHERE CPF = %s", (cpf,))
        conn.commit()

        print("\nFoto deletada com sucesso.\n")
        
    finally:
        cur.close()
        conn.close()