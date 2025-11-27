from pdf2docx import parse
import os
from pathlib import Path


def encontrar_arquivo(nome_arquivo, caminho_inicial):
    """Procura um arquivo recursivamente a partir de um diretório inicial."""
    caminho_inicial = Path(caminho_inicial)
    if not caminho_inicial.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {caminho_inicial}")
    
    for root, dirs, files in os.walk(caminho_inicial):
        if nome_arquivo in files:
            return Path(root) / nome_arquivo
    return None


def converter_pdf_para_docx(pdf_path, docx_path=None):
    """Converte um arquivo PDF para DOCX."""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
    
    if docx_path is None:
        docx_path = pdf_path.with_suffix('.docx')
    else:
        docx_path = Path(docx_path)
    
    try:
        parse(str(pdf_path), str(docx_path))
        return docx_path
    except Exception as e:
        raise RuntimeError(f"Erro ao converter PDF para DOCX: {e}")


def main():
    nome_arquivo = 'LIVRO_3_PPGTE_Emanoel_Lopes-final.pdf'
    caminho_da_pasta = '/home/emanoel/Downloads'
    
    # Encontrar o arquivo PDF
    arquivo_encontrado = encontrar_arquivo(nome_arquivo, caminho_da_pasta)
    
    if arquivo_encontrado is None:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado em '{caminho_da_pasta}'")
        return
    
    print(f'PDF encontrado: {arquivo_encontrado}')
    
    # Converter PDF para DOCX
    try:
        docx_file = converter_pdf_para_docx(arquivo_encontrado)
        print(f"Conversão realizada com sucesso!")
        print(f"  PDF: {arquivo_encontrado}")
        print(f"  DOCX: {docx_file}")
    except Exception as e:
        print(f"Erro durante a conversão: {e}")


if __name__ == "__main__":
    main()

