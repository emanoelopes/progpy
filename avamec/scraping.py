import requests
from bs4 import BeautifulSoup

url = "https://avamecinterativo.mec.gov.br/"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Exemplo: extrair todos os títulos das atividades
for titulo in soup.find_all("h3"):
    print(titulo.get_text(strip=True))