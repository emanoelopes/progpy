import numpy as np
import pandas as pd

def create_data():
    data = {
        "Aluno": [f"Aluno_{i+1}" for i in range(50)],
        "Números Inteiros": np.random.uniform(3.0, 10.0, 50).round(1),
        "Frações": np.random.uniform(3.0, 10.0, 50).round(1),
        "Equações": np.random.uniform(3.0, 10.0, 50).round(1),
        "Geometria Básica": np.random.uniform(3.0, 10.0, 50).round(1),
    }
    return pd.DataFrame(data)
