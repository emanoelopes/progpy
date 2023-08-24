lista_palavras = []

while True:
    palavra = input("Digite uma palavra ou zero para sair: ")
    if palavra == "0":
        break
    else:
        lista_palavras.append(palavra)
print(set(lista_palavras))
