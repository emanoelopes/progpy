# Dado uma sequência de números, calcule a soma e média dos números.
# ATENÇÃO: não vale usar a função sum() !

# Dado uma sequência de números, calcule o maior valor da sequência.
# ATENÇÃO: não vale usar a função max() !

# Dado uma lista de palavras, printe todas as palavras
# com pelo menos 5 caracteres.

sn = [1,2,5]
soma = 0
max = 0
palavras = ['Mestrado','Dissertação','Defesa']

for n in sn:
    soma += n

media = soma / len(sn)
    
print(f"Soma: {soma}, Média {media}")

for n in sn:
    if n > max:
        max = n

print(f"Maior valor: {max}")

print("Palavras com pelo menos 5 caracteres:")
for palavra in palavras:
    if len(palavra) >= 5:
        print(palavra)
