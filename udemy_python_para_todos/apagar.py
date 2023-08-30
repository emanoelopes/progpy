class Pai():
    def __init__(self, possui_carro, qtd):
      self.possui_carro = possui_carro
      self.qtd = qtd
    def passear(self):
        if self.possui_carro:
            print("Vai passear")
        else:
            print("Vai ficar em casa")
    def oficina(self):
        if self.possui_carro:
            print("Precisa oficina")
        else:
            print("Não precisa de oficina, pq não tem carro.")
    def lavar(self):
        print("Lavar o carro")
    def enxugar(self):
        print("Enxugar o carro")


class Motorista(Pai):
    def __init__(self, experiencia):
        super().__init__(True, experiencia)


class Veiculo:
    def __init__(self, possui_motor, qtd_rodas):
        self.possui_motor = possui_motor
        self.qtd_rodas = qtd_rodas
        self.ligado = False
    def ligar(self):
        if self.possui_motor:
            self.ligado = True
            print("Ligou")
        else:
            print("Não tem motor")
    def desligar(self):
        if self.possui_motor:
            if self.ligado:
                print("Desligou")
            else:
                print("Não está ligado.")
        else:
            print("Não tem motor")
    def andar(self):
        print("O veículo começou a andar")
    def parar(self):
        print("O veiculo parou")


class Carro(Veiculo):
    def __init__(self, qtd_rodas):
        super().__init__(True, 4)


class Bicicleta(Veiculo):
    possui_guidao = True

    def __init__(self, qtd_rodas):
        super().__init__(False, 2)
    def empinar(self):
        print("A bicicleta empinou")


bike = Bicicleta(2)
print(bike.possui_motor)
print(bike.possui_guidao)
print(bike.qtd_rodas)
bike.ligar()
bike.andar()
bike.empinar()
bike.parar()
bike.desligar()
car = Carro(4)
print(car.qtd_rodas)
car.desligar()
car.ligar()
car.andar()
car.parar()
car.desligar()

