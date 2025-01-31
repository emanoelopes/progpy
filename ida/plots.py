import matplotlib.pyplot as plt

def plot_scatter(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Números Inteiros"], df["Equações"], color='blue', alpha=0.6)
    plt.title('Relação entre Números Inteiros e Equações')
    plt.xlabel('Números Inteiros')
    plt.ylabel('Equações')
    plt.grid()
    plt.show()
