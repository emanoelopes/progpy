import csv
from typing import Iterable, List, Mapping, Optional, Sequence, Union

try:
    import pandas as pd
except Exception:  # pandas é opcional para tipos não-DataFrame
    pd = None


def gerar_csv(
    dados: Union["pd.DataFrame", Iterable[Mapping], Iterable[Sequence]],
    nome_arquivo: str,
    *,
    colunas: Optional[List[str]] = None,
    separador: str = ";",
    decimal: str = ",",
    incluir_indice: bool = False,
    encoding: str = "utf-8-sig",
    float_precision: str = "%.2f",
) -> None:
    """Gera um CSV com formatação consistente.

    - Usa separador ";" e decimal "," (compatível com Excel/pt-BR).
    - Força ordem de colunas se fornecida.
    - Em DataFrame, utiliza float_format e encoding UTF-8 BOM.
    - Em listas, escreve cabeçalho automaticamente.
    """

    # Caso DataFrame
    if pd is not None and isinstance(dados, pd.DataFrame):
        df = dados.copy()
        if colunas is not None:
            existentes = [c for c in colunas if c in df.columns]
            df = df[existentes]
        df.to_csv(
            nome_arquivo,
            sep=separador,
            decimal=decimal,
            index=incluir_indice,
            encoding=encoding,
            float_format=float_precision,
        )
        return

    # Caso lista de dicts ou lista de listas
    with open(nome_arquivo, "w", newline="", encoding=encoding) as arquivo_csv:
        if isinstance(dados, Iterable):
            dados = list(dados)
        if not dados:
            # arquivo vazio apenas com cabeçalho (se colunas fornecidas)
            if colunas:
                escritor = csv.writer(arquivo_csv, delimiter=separador)
                escritor.writerow(colunas)
            return

        # Deduzir cabeçalhos
        if isinstance(dados[0], Mapping):
            headers = colunas or list(dados[0].keys())
            escritor = csv.DictWriter(
                arquivo_csv,
                fieldnames=headers,
                delimiter=separador,
                quoting=csv.QUOTE_MINIMAL,
            )
            escritor.writeheader()
            for row in dados:
                escritor.writerow({k: row.get(k, "") for k in headers})
        else:
            escritor = csv.writer(arquivo_csv, delimiter=separador)
            if colunas:
                escritor.writerow(colunas)
            escritor.writerows(dados)

