from pathlib import Path


def gerar_eda(df, saida_html: str) -> str:
    """Gera um relatório EDA em HTML usando ydata-profiling.

    Retorna o caminho absoluto do arquivo salvo.
    """
    try:
        from ydata_profiling import ProfileReport
    except Exception as exc:
        raise RuntimeError("ydata-profiling não está instalado. Instale as dependências.") from exc

    saida_path = Path(saida_html)
    saida_path.parent.mkdir(parents=True, exist_ok=True)

    # Evita erros de WordCloud/Pillow removendo colunas de texto (ex.: "Aluno")
    df_profile = df.select_dtypes(exclude=["object"]).copy()
    if df_profile.empty:
        # Se tudo era texto, volta ao original mas com amostra mínima
        df_profile = df.copy()

    try:
        profile = ProfileReport(
            df_profile,
            title="EDA - Perfil do Dataset",
            explorative=True,
            correlations={
                "pearson": {"calculate": True},
                "spearman": {"calculate": True},
                "kendall": {"calculate": False},
                "phi_k": {"calculate": False},
                "cramers": {"calculate": False},
            },
            interactions={"continuous": True},
            duplicates={"head": 10},
            samples={"head": 20},
            missing_diagrams={"heatmap": True, "dendrogram": False},
        )
        profile.to_file(str(saida_path))
    except Exception:
        # Fallback ultra-minimalista se algo falhar (ex.: issue com Pillow/WordCloud)
        profile = ProfileReport(
            df_profile,
            title="EDA - Perfil do Dataset (Minimal)",
            explorative=False,
            correlations={"pearson": {"calculate": False}},
            interactions={"continuous": False},
            duplicates={"head": 5},
            samples={"head": 10},
            missing_diagrams={"heatmap": False, "dendrogram": False},
        )
        profile.to_file(str(saida_path))
    return str(saida_path.resolve())


