texto1 = input("Digite o texto 1: ")
texto2 = input("Digite o texto 2: ")

print(f"texto 1 : {texto1}")
print(f"texto 2 : {texto2}")
print(f"Quantidade de caracteres de '{texto1}':", len(texto1))
print(f"Quantidade de caracteres de '{texto2}':", len(texto2))
print(f"As strings possuem a mesma quantidade de caracteres? ",
      len(texto1) == len(texto2))
print(f"As strings são iguais? ", texto1 == texto2)
