"""
AUTOMATIZAR O ENVIO DE MENSGAS PARA OS ATTs POR MEIO DO WHATSAPP
Dependências: openpyxl, pillow, pyautogui, opencv-python, webbrowser, urllib.parse, time

"""
import webbrowser
import openpyxl
from urllib.parse import quote
from time import sleep
import pyautogui

workbook = openpyxl.load_workbook('atts.xlsx')
pagina_atts = workbook['Sheet1']
# # Abrir o WhatsApp Web no navegador
# print("Abrindo o WhatsApp Web...")
# webbrowser.open('https://web.whatsapp.com/')
# # Aguardar o usuário escanear o QR code do WhatsApp Web
# sleep(20)  # Espera 10 segundos para o usuário escanear o QR code
# print("QR code escaneado, continuando...")
# # Percorrer as linhas da planilha e enviar mensagens
print("Iniciando o envio de mensagens...")
for linha in pagina_atts.iter_rows(min_row=2):
    nome = linha[0].value
    telefone = linha[1].value
    print(nome)
    print(telefone)
    mensagem = f'Olá {nome}, tudo bem? Essa é uma mensagem automatizada 25.'
    # print(f"Enviando mensagem para {nome}: {mensagem}")
    link_mensagem_whatsapp = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
    webbrowser.open(link_mensagem_whatsapp)
    sleep(20)  # Espera 5 segundos para garantir que a página carregou
    try:
        seta = pyautogui.locateCenterOnScreen('seta.png', confidence=0.8)  # Tenta localizar a imagem da seta na tela com maior tolerância
        if seta is None:
            raise Exception("Seta não encontrada na tela. Verifique se 'seta.png' está no diretório correto e visível na tela.")
        sleep(5)  # Espera 5 segundos para garantir que a seta foi localizada
        pyautogui.click(seta[0], seta[1])  # Clica na seta para enviar a mensagem
        sleep(5)  # Espera para garantir que a mensagem foi enviada
        pyautogui.hotkey('ctrl', 'w')  # Fecha a aba do navegador
        sleep(5)  # Espera 5 segundos antes de continuar para a próxima mensagem
        print(f'Mensagem enviada para {nome}!')
    except:
        print(f"Erro ao enviar mensagem para {nome}.")
        with open('erros.csv', 'a', newline='', encoding='utf-8') as arquivo_erros:
            arquivo_erros.write(f"Erro ao enviar mensagem para {nome}, ({telefone})\n")
        continue
