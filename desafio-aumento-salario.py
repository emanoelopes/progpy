salario_atual = float(input("Digite o valor do salário atual: "))
percentual_aumento = float(input("Digite o percentual de aumento: "))
salario_atualizado = salario_atual + (
    (salario_atual * percentual_aumento) / 100.00)
print(f"O valor do salario atualizado é: {salario_atualizado:,.2f}")
