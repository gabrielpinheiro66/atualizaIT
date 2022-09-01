import verify
from config import pastas_conf
from time import sleep
from functions import logging


def run(secao, lista_de_pasta):
    erro = False
    pasta_adm = lista_de_pasta[0]
    pasta_local = lista_de_pasta[1]
    pasta_teste = lista_de_pasta[2]
    print("\n")
    logging("==================================")
    logging(f"Secao: {secao}")
    logging(f"Pasta ADM: {pasta_adm}")
    logging(f"Pasta LOCAL: {pasta_local}")
    logging(f"Pasta TESTE: {pasta_teste}")
    print("\n\n")
    logging("------ Pasta ADM para LOCAL: ------")
    print("\n\n")
    try:
        verify.tree(pasta_adm, pasta_local, False)
    except Exception as e:
        logging(f"Erro em pasta adm para local - {e}")
        erro = True
    # end
    print("\n\n")
    logging("------ Pasta LOCAL para TESTE: ------")
    print("\n\n")
    try:
        verify.tree(pasta_local, pasta_teste, True)
    except Exception as e:
        logging(f"Erro em pasta local para teste - {e}")
        erro = True
    return erro


def main():
    while True:
        secoes, pastas = pastas_conf()
        loops = len(secoes)
        erros = []
        for i in range(loops):
            erro = run(secoes[i], pastas[i])
            erros.append(erro)
        if not (True in erros):
            logging(f"Os arquivos das pastas {[secao for secao in secoes]} estao iguais entre os dois servidores ")
        sleep(600)
        #break


if __name__ == '__main__':
    main()
