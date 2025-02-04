from data import create_data
from models import evaluate_models
from prerequisite_issues import identify_prerequisite_issues

def main():
    # Criando o DataFrame
    df = create_data()

    # Avaliar modelos
    metrics = evaluate_models(df)
    
if __name__ == "__main__":
    main()
