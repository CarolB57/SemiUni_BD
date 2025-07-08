'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

from participante import *
from certificado import *
from definicoes import *
from inscricao import *
from foto import *

console = Console()

def menu():
    while True:
        print("\n")
        console.print(Panel.fit(
            "[bold cyan]Menu Principal[/bold cyan]\n\n"
            "[bold yellow]1.[/] Participante\n"
            "[bold yellow]2.[/] Inscrição\n"
            "[bold yellow]3.[/] Certificado\n"
            "[bold yellow]4.[/] Listar atividades disponíveis\n"
            "[bold yellow]5.[/] Listar cursos disponíveis\n"
            "[bold yellow]6.[/] Sair",
            title="Semana Universitária"
        ))

        print("Escolha uma opção: ", end="")
        opcao = ler_inteiro(1, 6)
        print("\n")

        if opcao == 1:
            console.print(Panel.fit(
                "[bold cyan]Participante[/bold cyan]\n\n"
                "[bold yellow]1.[/] Criar Participante\n"
                "[bold yellow]2.[/] Listar Participantes\n"
                "[bold yellow]3.[/] Atualizar Participante\n"
                "[bold yellow]4.[/] Deletar Participante\n"
                "[bold yellow]5.[/] Inserir foto de participante\n"
                "[bold yellow]6.[/] Recuperar foto de participante\n"
                "[bold yellow]7.[/] Deletar foto de participante\n"
                "[bold yellow]8.[/] Voltar",
                title="Menu Participante"
            ))
            print("Escolha uma opção: ", end="")
            op = ler_inteiro(1, 8)
            print("\n")
            if op == 1:
                criar_participante()
            elif op == 2:
                listar_participantes()
            elif op == 3:
                atualizar_participante()
            elif op == 4:
                deletar_participante()
            elif op == 5:
                inserir_foto()
            elif op == 6:
                salvar_foto()
            elif op == 7:
                deletar_foto()

        elif opcao == 2:
            console.print(Panel.fit(
                "[bold cyan]Inscrição[/bold cyan]\n\n"
                "[bold yellow]1.[/] Criar Inscrição\n"
                "[bold yellow]2.[/] Listar Inscrições\n"
                "[bold yellow]3.[/] Atualizar Inscrição\n"
                "[bold yellow]4.[/] Deletar Inscrição\n"
                "[bold yellow]5.[/] Voltar",
                title="Menu Inscrição"
            ))
            print("Escolha uma opção: ", end="")
            op = ler_inteiro(1, 5)
            print("\n")
            if op == 1:
                criar_inscricao()
            elif op == 2:
                listar_inscricoes()
            elif op == 3:
                atualizar_inscricao()
            elif op == 4:
                deletar_inscricao()

        elif opcao == 3:
            console.print(Panel.fit(
                "[bold cyan]Certificado[/bold cyan]\n\n"
                "[bold yellow]1.[/] Criar Certificado\n"
                "[bold yellow]2.[/] Listar Certificados\n"
                "[bold yellow]3.[/] Atualizar Certificado\n"
                "[bold yellow]4.[/] Deletar Certificado\n"
                "[bold yellow]5.[/] Voltar",
                title="Menu Certificado"
            ))
            print("Escolha uma opção: ", end="")
            op = ler_inteiro(1, 5)
            print("\n")
            if op == 1:
                criar_certificado()
            elif op == 2:
                listar_certificados()
            elif op == 3:
                atualizar_certificado()
            elif op == 4:
                deletar_certificado()

        elif opcao == 4:
            listar_atividades()

        elif opcao == 5:
            listar_cursos()

        elif opcao == 6:
            console.print("\n[bold green]Encerrando o programa. Obrigado por utilizar este banco de dados![/bold green]\n")
            break

if __name__ == "__main__":
    menu()

