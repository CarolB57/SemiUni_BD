'''


Aluna: Caroline Bohadana Rodrigues Viana
Matrícula: 232050975

Trabalho Final de Banco de Dados


'''

from datetime import date

cursos = {
    746331003: "Ciência da Computação",
	993746282: "Engenharia de Produção",
	546378728: "Sociologia",
    298234736: "Engenharia Elétrica",
	873648364: "Engenharia Civil",
}

atividades = {
    839201: { 
        "nome": "Game Jam 2025",
        "datainicio": date(2025, 11, 10),
        "datafim": date(2025, 11, 14)
    },
    573920: {
        "nome": "Feira de Inovação Tecnológica (FIT) da Faculdade UnB Gama",
        "datainicio": date(2025, 11, 12),
        "datafim": date(2025, 11, 12)
    },
    675849: {
        "nome": "Mesa de Abertura SEMUNI 2025",
        "datainicio": date(2025, 11, 11),
        "datafim": date(2025, 11, 11)
    },
    394754: {
        "nome": "Edubot - Oficina de Robótica Móvel",
        "datainicio": date(2025, 11, 12),
        "datafim": date(2025, 11, 13)
    },
    938475: {
        "nome": "COPA DAS EDOS NAS ESTAÇÕES",
        "datainicio": date(2025, 11, 14),
        "datafim": date(2025, 11, 14)
    }
}