from data import create_data
from sklearn.model_selection import train_test_split
from prerequisite_issues import identify_prerequisite_issues

def main():
    # Criando o DataFrame
    df, pre_reqs = create_data()

    # Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Chamar a função identidy_prerequisite_issues com pre_reqs gerado e data.py
    recommendations, metrics_summary = identify_prerequisite_issues(df, pre_reqs)

    # Avaliar modelos
    # metrics = evaluate_models(df)

    # Exibir os resultados
    print("Recomendações:", recommendations)
    print("\nResumo das Métricas:", metrics_summary)

    
if __name__ == "__main__":
    main()
