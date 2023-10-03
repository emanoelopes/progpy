import os.path

while True:
    nome = input("Informe um nome de arquivo ou pasta (informe 'sair' para finalizar): ")
    if nome.upper() == "SAIR":
        break
    if os.path.exists(nome):
        print(nome, "existe")
        if os.path.isdir(nome):
            print(nome, "é um diretório")
        elif os.path.isfile(nome):
            print(nome, "é um arquivo")
    else:
        print(nome, "não existe")


