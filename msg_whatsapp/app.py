"""
AUTOMATIZAR O ENVIO DE MENSGAS PARA O WHATSAPP

requirementos: openpyxl, 

"""
import openpyxl

workbook = openpyxl.load_workbook('atts.xlsx')
pagina_atts = workbook['Sheet1']

for linha in pagina_atts.iter_rows(min_row=2, values_only=True):
    nome = linha[0].value
    telefone = linha[1].value

    print(nome, telefone)
    
    # Aqui você pode adicionar o código para enviar a mensagem via WhatsApp
    # Por exemplo, usando uma API de WhatsApp ou uma biblioteca específica
    print(f"Enviando mensagem para {nome}: {mensagem}")
