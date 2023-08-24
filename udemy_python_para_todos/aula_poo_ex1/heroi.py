class Heroi:
    """
    Classe de heróis
    """
    def __init__(self, voa, possui_arma, lanca_teia, frase_comum):
        print("Inicializando...")
        self.voa = voa
        self.lanca_teia = lanca_teia
        self.possui_arma = possui_arma
        self.frase_comum = frase_comum

    def falar(self):
        print(self.frase_comum)

    def detalhar(self):
        if self.voa:
            print("O heróie voa")
        if self.lanca_teia:
            print("O herói voa")
        if self.possui_arma:
            print("Possui arma")
