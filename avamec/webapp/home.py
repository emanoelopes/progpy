import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Dados fictícios de rotatividade de clientes
data = {
    'Mês': ['Outubro'],
    'Clientes Perdidos': [43]
}

df = pd.DataFrame(data)

# Título do aplicativo
st.title('Evasão de Cursistas por Mês')

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x='Mês', y='Clientes Perdidos', data=df, palette='viridis')
plt.title('Evasão de cursistas por Mês')
plt.xlabel('Mês')
plt.ylabel('Cursistas Evadidos')

# Exibindo o gráfico no Streamlit
st.pyplot(plt)