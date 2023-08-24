def maior_valor(valores):
    return max(valores)


def capturar_numeros():
    lista_numeros = []
    while True:
        numero = int(input("Informe um número inteiro ou zero para sair: "))
        if numero == 0:
            break
        lista_numeros.append(numero)
    return maior_valor(lista_numeros)


print(f"Maior valor: {capturar_numeros()}")
