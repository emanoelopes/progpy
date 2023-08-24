status = int(input("Digite o codigo do status(1-4): "))
num_malas = int(input("Digite o número de malas: "))

if ((status == 1 and num_malas > 1) or (status == 2 and num_malas > 2)
        or ((status == 3 or status == 4) and num_malas > 3)):
    print("Você terá de pagar uma taxa de serviço por excesso de bagagem")
else:
    comprimento = int(input("digite o comprimento: "))
    largura = int(input("digite a largura: "))
    altura = int(input("digite o altura: "))
    peso = int(input("digite o peso: "))
