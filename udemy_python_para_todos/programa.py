from pessoa_compilada import Pessoa

p = Pessoa("José")


def pegar_nome(self):
    """ Não existe esta função na classe Pessoa compilada """
    return self.nome

def mudar_nome(self, novo_nome):
    """ Agora vamos mudar o nome que foi passado como parâmetro na criação do objeto """
    self.nome = novo_nome


Pessoa.pegar_nome = pegar_nome
Pessoa.mudar_nome = mudar_nome

p.mudar_nome("André")


Pessoa.sobre_nome = "Teixeira"

def imprimir_ola(self):
    print("Olá", self.nome, self.sobre_nome)


Pessoa.ola = imprimir_ola


p.ola()


