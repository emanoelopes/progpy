"""
SCRIPT PARA AUTOMATIZAR O ENVIO DE MENSGAS PARA OS CURSISTAS E ATTs POR MEIO DO WHATSAPP
Dependências:

pip install openpyxl pillow pyautogui opencv-python webbrowser urllib.parse time

"""
import webbrowser
import openpyxl
from urllib.parse import quote
from time import sleep
import pyautogui

workbook = openpyxl.load_workbook('contatos.xlsx')
pagina_atts = workbook['Sheet2']
# # Abrir o WhatsApp Web no navegador
# print("Abrindo o WhatsApp Web...")
# webbrowser.open('https://web.whatsapp.com/')
# # Aguardar o usuário escanear o QR code do WhatsApp Web
# sleep(20)  # Espera 10 segundos para o usuário escanear o QR code
# print("QR code escaneado, continuando...")
# # Percorrer as linhas da planilha e enviar mensagens
print("Iniciando o envio de mensagens...")
for linha in pagina_atts.iter_rows(min_row=2):
    # Verifica se a linha está nula (todos os valores são None)
    if all(cell.value is None for cell in linha):
        print("Linha nula encontrada. Encerrando o programa.")
        break

    nome = linha[0].value
    telefone = linha[1].value
    print(nome)
    print(telefone)
    mensagem = (
        "*Prorrogação do Prazo para Confirmação da Inscrição para 31/07/2025*\n\n"
        f"Olá {nome},\n\n"
        "Seu nome foi indicado pela Secretaria Municipal de Educação para participar do Curso de Aperfeiçoamento em Mentoria de Diretores Escolares.\n\n"
        "⚠️ *Ainda NÃO recebemos a confirmação da sua matrícula!* ⚠️\n"
        "A confirmação deve ser feita exclusivamente pelo link abaixo até *31/07/2025*. Após essa data, sua vaga será destinada a outro município.\n\n"
        "👉 Link para confirmação de matrícula:\n"
        "https://forms.gle/WAKzih3nE5Tyho22A\n\n"
        "Em caso de dúvidas, entre em contato pelo e-mail:\n"
        "proditec-alunos@virtual.ufc.br\n\n"
        "Mais informações podem ser lidas no e-mail encaminhado.\n\n"
        "Henrique Barbosa Silva\n"
        "Coordenação Administrativa do Curso em Mentoria de Diretores Escolares\n"
        "Universidade Federal do Ceará"
    )
    link_mensagem_whatsapp = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
    webbrowser.open(link_mensagem_whatsapp)
    sleep(20)  # Espera 5 segundos para garantir que a página carregou
    try:
        seta = pyautogui.locateCenterOnScreen('seta.png', confidence=0.8)  # Tenta localizar a imagem da seta na tela com maior tolerância
        if seta is None:
            raise Exception("Seta não   encontrada na tela. Verifique se 'seta.png' está no diretório correto e visível na tela.")
        sleep(8)  # Espera 5 segundos para garantir que a seta foi localizada
        pyautogui.click(seta[0], seta[1])  # Clica na seta para enviar a mensagem
        sleep(8)  # Espera para garantir que a mensagem foi enviada
        pyautogui.hotkey('ctrl', 'w')  # Fecha a aba do navegador
        sleep(8)  # Espera 5 segundos antes de continuar para a próxima mensagem
        print(f'Mensagem enviada para {nome}!')
    except:
        print(f"Erro ao enviar mensagem para {nome}.")
        with open('erros.csv', 'a', newline='', encoding='utf-8') as arquivo_erros:
            arquivo_erros.write(f"Erro ao enviar mensagem para {nome}, ({telefone})\n")
        continue
