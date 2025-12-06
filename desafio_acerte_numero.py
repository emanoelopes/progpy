# Desafio - crie um programa que:
# - Escolhe um número secreto.
# - Pede por um chute do usuário.
# - Indica se o usuário acertou ou não.
# - Se não acertou, dá uma dica, dizendo
#   - se o número é mais alto ou mais baixo.
# - Repete isso até 3 vezes!

numero_secreto = 10
descobriu = False

if not descobriu:
    chute = int(input('Descubra o número!\n Seu chute: '))
    if chute < numero_secreto:
        print('Chute muito baixo!')
    elif chute > numero_secreto:
        print('Chute muito alto!')
    else:
        print('Descobriu o número! Parabéns!')
        descobriu = True

if not descobriu:
    chute = int(input('Descubra o número!\n Seu chute: '))
    if chute < numero_secreto:
        print('Chute muito baixo!')
    elif chute > numero_secreto:
        print('Chute muito alto!')
    else:
        print('Descobriu o número! Parabéns!')
        descobriu = True

if not descobriu:
    chute = int(input('Descubra o número!\n Seu chute: '))
    if chute < numero_secreto:
        print('Chute muito baixo!')
    elif chute > numero_secreto:
        print('Chute muito alto!')
    else:
        print('Descobriu o número! Parabéns!')
        descobriu = True

if descobriu:
    print('Parabéns, você ganho!')
else:
    print(f'Você perdeu! O número secreto era {numero_secreto}.')