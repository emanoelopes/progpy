from data import create_data
from sklearn.model_selection import train_test_split
from prerequisite_issues import identify_prerequisite_issues
from output import gerar_csv

def main():
    # Criando o DataFrame
    df, pre_reqs = create_data()

    # Identificando os pré-requisitos que os alunos precisam melhorar
    recommendations, metrics_summary = identify_prerequisite_issues(df, pre_reqs)

    # Avaliar modelos
    # metrics = evaluate_models(df)

    # Exibir os resultados
    print("Recomendações:", recommendations)
    print("\nResumo das Métricas:", metrics_summary)

    # Criando um arquivo csv com os resultados
    gerar_csv(df, 'output.csv')

if __name__ == "__main__":
    main()
