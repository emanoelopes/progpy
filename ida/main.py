from data import create_data
from models import evaluate_models
from plots import plot_scatter

def main():
    # Criar dados
    df = create_data()

    # Avaliar modelos
    metrics = evaluate_models(df)
    print("Métricas dos Modelos:", metrics)
    
    # Gerar gráfico de dispersão
    plot_scatter(df)

if __name__ == "__main__":
    main()
