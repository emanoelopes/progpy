import requests
from bs4 import BeautifulSoup
from rich.console import Console

URL_DOWNLOADS = "https://clonezilla.org/downloads.php"
CONSOLE = Console()

def obter_info_ultima_versao():
    try:
        response = requests.get(URL_DOWNLOADS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Seletor para a versão (manter o que você encontrou)
        versao_elemento = soup.select_one("div.innertube:nth-child(2) > center:nth-child(4) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > a:nth-child(1) > font:nth-child(2)")
        ultima_versao = versao_elemento.get_text(strip=True) if versao_elemento else None

        modificacoes = []
        # Tentar encontrar um link para as notas de lançamento (isso pode variar)
        changelog_link_elemento = soup.select_one("div.innertube:nth-child(2) > center:nth-child(4) > p:nth-child(5) > a:nth-child(1)") # Exemplo de um possível link

        if changelog_link_elemento and "changelog" in changelog_link_elemento.get("href", ""):
            changelog_url = "https://clonezilla.org/" + changelog_link_elemento["href"]
            CONSOLE.print(f"[yellow]Encontrei um link para o changelog: {changelog_url}[/yellow]")
            changelog_response = requests.get(changelog_url)
            changelog_response.raise_for_status()
            changelog_soup = BeautifulSoup(changelog_response.content, 'html.parser')

            # Adaptar este seletor para encontrar a lista de modificações da ÚLTIMA versão
            # A estrutura da página de changelog pode variar muito
            changelog_items = changelog_soup.select("div.content > ul:nth-child(2) > li") # Exemplo: lista dentro de uma div 'content'

            if changelog_items:
                for item in changelog_items[:5]: # Pegar as 5 primeiras como exemplo
                    modificacoes.append(item.get_text(strip=True))
            else:
                CONSOLE.print("[red]Não consegui encontrar a lista de modificações na página de changelog com o seletor atual.[/red]")
        else:
            CONSOLE.print("[yellow]Não encontrei um link direto para o changelog na página de downloads.[/yellow]")
            # Tentar encontrar modificações diretamente na página de downloads (improvável)
            # Você precisaria inspecionar a página e criar um seletor específico aqui
            pass

        return ultima_versao, modificacoes

    except requests.exceptions.RequestException as e:
        CONSOLE.print(f"[bold red]Erro ao acessar o site:[/bold red] {e}")
        return None, []
    except Exception as e:
        CONSOLE.print(f"[bold red]Erro ao processar a página:[/bold red] {e}")
        return None, []

if __name__ == "__main__":
    versao, modificacoes = obter_info_ultima_versao()
    if versao:
        CONSOLE.print(f"[bold green]Última Versão Encontrada:[/bold green] {versao}")
        if modificacoes:
            CONSOLE.print("[bold yellow]Principais Modificações:[/bold yellow]")
            for i, mod in enumerate(modificacoes, 1):
                CONSOLE.print(f"{i}. {mod}")
        else:
            CONSOLE.print("[yellow]Não foram encontradas modificações.[/yellow]")
    else:
        CONSOLE.print("[bold red]Não foi possível obter a informação da última versão.[/bold red]")
