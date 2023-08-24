num1 = int(input("Informe o número 1: "))
num2 = int(input("Informe o número 2: "))
primeira_operacao = int(
    input(f"Informe o resultado da operacao: {num1} + {num2} = "))
if primeira_operacao == num1 + num2:
    print("Resposta correta")
else:
    print(f"Resposta incorreta. A resposta de {num1} + {num2} = ", num1 + num2)
segunda_operacao = int(
    input(f"Informe o resultado da operação: {num1} - {num2} = "))
if segunda_operacao == num1 - num2:
    print("Resposta correta")
else:
    print(f"Resposta correta de {num1} - {num2} =", num1 - num2)
terceira_operacao = int(
    input(f"Informe o resultado da operacao: {num1} * {num2} = "))
if terceira_operacao == num1 * num2:
    print("Resposta correta")
else:
    print(f"A resposta de {num1} * {num2} = ", num1 * num2)
quarta_operacao = float(
    input(f"Informe o resultado da operacao: {num1} * {num2} = "))
if quarta_operacao == num1 / num2:
    print("Resposta correta")
else:
    print(f"A resposta de {num1} / {num2} = {num1/num2:,.2f}")
