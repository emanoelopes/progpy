valor = input("Informe um número")

try:
    soma = int(valor) + 10
    resultado = soma / int(valor)
except ZeroDivisionError:
    print("Ocorreu um erro de divisão por zero.")
except ValueError:
    print("Ocorreu um erro de valor.")

