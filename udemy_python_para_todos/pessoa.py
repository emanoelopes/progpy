class Pessoa():
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


class Pessoa_fisica(Pessoa):
    def __init__(self, cpf, nome, idade):
        super().__init__(nome, idade)
        self.cpf = cpf


class Pessoa_juridica(Pessoa):
    def __init__(self, cnpj, nome, idade):
        super().__init__(nome, idade)
        self.cnpj = cnpj


pf = Pessoa_fisica("092.098.982-11", "Fulano", 44)
pj = Pessoa_juridica("01.111.111/0001-88", "Empresa", 5)

print(pf.idade)
print(pj.cnpj)


