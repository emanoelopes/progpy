class RevelarAcesso:
    def __init__(self, initval=None, name="val"):
        self.val = initval
        self.name = name

    def __get__(self, instance, value):
        print("Recuperando", self.name)
        return self.val

    def __set__(self, instance, value):
        print("Atualizando", self.name)
        self.val = value


class MinhaClasse:
    x = RevelarAcesso(10, "val 'x'")
    y = 5


m = MinhaClasse()

print("x:", m.x)
m.x = 20
print("x:", m.x)

print("y:", m.y)
m.y = 9
print("y:", m.y)
