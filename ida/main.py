import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from data import create_data
from prerequisite_issues import identify_prerequisite_issues
from output import gerar_csv
from output import gerar_csv


def build_metrics_dataframe(metrics_summary):
    rows = []
    for subject, models_metrics in metrics_summary.items():
        for model_name, metrics in models_metrics.items():
            rows.append({
                "Disciplina": subject,
                "Modelo": model_name,
                "MAE": metrics.get("MAE"),
                "MSE": metrics.get("MSE"),
                "R2": metrics.get("R²"),
            })
    if not rows:
        return pd.DataFrame(columns=["Disciplina", "Modelo", "MAE", "MSE", "R2"])
    df = pd.DataFrame(rows)
    return df.sort_values(["Disciplina", "R2"], ascending=[True, False])


def build_recommendations_dataframe(recommendations, top_n):
    recs_rows = []
    for aluno, recs in recommendations.items():
        for req, imp in recs[:top_n]:
            recs_rows.append({"Aluno": aluno, "Pré-requisito": req, "Importância": imp})
    if not recs_rows:
        return pd.DataFrame(columns=["Aluno", "Pré-requisito", "Importância"])
    return pd.DataFrame(recs_rows)


def maybe_plot(metrics_df, show_plots):
    if not show_plots:
        return
    try:
        import seaborn as sns
        pivot = metrics_df.pivot_table(index="Disciplina", columns="Modelo", values="R2")
        if pivot.size == 0:
            return
        sns.heatmap(pivot, annot=True, fmt=".2f", cmap="Blues")
        plt.title("R² por Disciplina e Modelo")
        plt.tight_layout()
        plt.show()
    except Exception:
        # Plotting is optional; ignore failures
        pass


def save_artifacts(metrics_df, recs_df, save):
    if not save:
        return
    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    metrics_df.to_csv(out / "metrics.csv", index=False)
    recs_df.to_csv(out / "recommendations.csv", index=False)
    metrics_df.to_json(out / "metrics.json", orient="records")
    recs_df.to_json(out / "recommendations.json", orient="records")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=5.0)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()

    # Criando o DataFrame
    df, pre_reqs = create_data()

    # Identificando os pré-requisitos que os alunos precisam melhorar
    recommendations, metrics_summary = identify_prerequisite_issues(df, pre_reqs, threshold=args.threshold)

    # Formatar e exibir métricas
    pd.options.display.float_format = "{:.3f}".format
    metrics_df = build_metrics_dataframe(metrics_summary)
    print("\nMétricas por disciplina e modelo:")
    print(metrics_df.to_string(index=False))

    # Formatar e exibir recomendações (top N)
    recs_df = build_recommendations_dataframe(recommendations, args.top)
    print("\nRecomendações (top {} por aluno):".format(args.top))
    print(recs_df.to_string(index=False))

    # Plots opcionais
    maybe_plot(metrics_df, show_plots=not args.no_plots)

    # Exportar artefatos
    save_artifacts(metrics_df, recs_df, save=args.save)

    # Criar um CSV unificado e amigável (output.csv)
    # Colunas padronizadas para unir métricas e recomendações em formato "long"
    unified_cols = [
        "Tipo", "Disciplina", "Modelo", "MAE", "MSE", "R2",
        "Aluno", "Pré-requisito", "Importância"
    ]

    metrics_long = metrics_df.copy()
    metrics_long.insert(0, "Tipo", "Métrica")
    for col in ["Aluno", "Pré-requisito", "Importância"]:
        if col not in metrics_long.columns:
            metrics_long[col] = ""

    recs_long = recs_df.copy()
    recs_long.insert(0, "Tipo", "Recomendação")
    for col in ["Disciplina", "Modelo", "MAE", "MSE", "R2"]:
        if col not in recs_long.columns:
            recs_long[col] = ""

    unified_df = pd.concat([metrics_long, recs_long], ignore_index=True, sort=False)
    # Reordenar colunas e gerar CSV com separador ; e decimal ,
    unified_df = unified_df[[c for c in unified_cols if c in unified_df.columns]]
    gerar_csv(unified_df, "output.csv", colunas=unified_cols)
    print("Arquivo CSV 'output.csv' criado com sucesso.")


if __name__ == "__main__":
    main()
