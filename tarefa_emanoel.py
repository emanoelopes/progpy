nome = input("Informe seu nome: ")
print("Obrigado por responder à pergunta",nome)

bebida = input("Qual bebida você prefere?\n"
        "1) Água\n"
        "2) Cerveja\n"
        "3) Vinho\n"
        "4) Leite\n"
        "Informe o número: ")
print("Você escolheu a opção: ",bebida)

nascimento = int(input("Em qual ano você nasceu?"))
idade = 2023 - nascimento
print("Você tem", idade,"anos")

salario_minimo = float(input("Informe o valor do salário mínimo:"))
pretensao = float(input("Quantos salários você deseja receber?"))
print("Você pretende receber R$ ",pretensao * salario_minimo)


salario = int(input("Qual o seu salário? "))
print(salario > salario_minimo * 2.0 and idade > 18)
