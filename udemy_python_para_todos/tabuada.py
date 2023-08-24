acerto = 0
erro = 0
num = int(input("Informe um número inteiro: "))
for i in range(1,11):
    resposta = int(input(f"Quanto é {num} x {i}?"))
    if resposta != (num*i):
        print("A respota correta é: ", num, 'x', i, '=', num * i)
        erro = erro + 1
    else: 
        print("Correto")
        acerto = acerto + 1
        print("Total de erros: ",erro)
    print("Total de erros: ", erro)
    print("Total de acertos: ",acerto)