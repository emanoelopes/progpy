texto = """

Pessoal, tudo bem?

Tenho algumas automações que rodam com PyAutoGui e elas estão rodando em uma VM.
O problema que as vezes ocorre é que se eu não ficar conectado na VM a automação não roda, como se precisa-se ter a interface visual ativa para funcionar.

Alguém já passou por isso e tem alguma dica de solução?
"""
vogais = {
    'A': 0,
    'E': 0,
    'I': 0,
    'O': 0,
    'U': 0
}

for caractere in texto:
    if caractere.upper() == 'A':
        vogais['A'] += 1
    if caractere.upper() == 'E':
        vogais['E'] += 1    
    if caractere.upper() == 'I':
        vogais['I'] += 1
    if caractere.upper() == 'O':
        vogais['O'] += 1
    if caractere.upper() == 'U':
        vogais['U'] += 1


for vogal, contagem in vogais.items():
    print(f'Há {contagem} letras {vogal} no texto')
    
