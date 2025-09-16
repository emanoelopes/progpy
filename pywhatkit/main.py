import pywhatkit
import time
import csv

# Lê os números do arquivo CSV (um número por linha)
numeros = []
with open('numeros.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:  # Ignora linhas vazias
            numeros.append(row[0].strip())

mensagem = "Olá! Esta é uma mensagem automática."

hora = 18 # Hora inicial
minuto = 25 # Minuto inicial

for i, numero in enumerate(numeros):
    pywhatkit.sendwhatmsg(numero, mensagem, hora, minuto + i, wait_time=10, tab_close=False)
    time.sleep(10)  # Aguarda para evitar sobreposição de envios

print("Mensagens enviadas com sucesso!")