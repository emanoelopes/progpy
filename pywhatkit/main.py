import pywhatkit
import time

# Lista de números no formato '+5511999999999'
numeros = [
    '+5585997489610',
    #'+5585988099872'
    # ...adicione até 200 números...
]

mensagem = "Olá! Esta é uma mensagem automática."

hora = 17  # Hora inicial
minuto = 52 # Minuto inicial

for i, numero in enumerate(numeros):
    pywhatkit.sendwhatmsg_instantly(numero, mensagem, hora, minuto + i)
    time.sleep(10)  # Aguarda para evitar sobreposição de envios

#pywhatkit.sendwhatmsg_instantly("+5585997489610", "Mensagem enviada com sucesso!", hora, minuto + len(numeros), tab_close=True)
print("Mensagens enviadas com sucesso!")