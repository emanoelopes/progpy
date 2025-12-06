# Dado duas listas, printe todos os valores que aparecerem
# duplicados nas duas listas.

lista1 = ['4','7','9','11', '88']
lista2 = ['9','8','90','88']

for valor1 in lista1:
    for valor2 in lista2:
        if valor1 == valor2:
            print(f"Elemento(s) em ambas listas encontrado(s): {valor1}")


# Dado duas listas, printe uma mensagem dizendo se existe
# algum elemento em comum entre elas ou não.

elemento_em_comum =  False

for valor1 in lista1:
    if elemento_em_comum:
        break
    for valor2 in lista2:
        if valor1 == valor2:
            elemento_em_comum = True
            break

if elemento_em_comum:
    print('As listas têm elementos em comum.')
else:
    print('As listas não têm elementos em comum.')
