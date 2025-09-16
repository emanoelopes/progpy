import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="SIDA Analysis", layout="wide")
st.title("Sistema de Identificação de Dificuldades de Aprendizagem (SIDA)")
st.markdown("""
O Sistema de Identificação de Dificuldades de Aprendizagem (SIDA) é uma ferramenta desenvolvida para auxiliar educadores e profissionais da área de educação a identificar e analisar dificuldades de aprendizagem em estudantes.
""")

@st.cache_data
def load_data():
    # Simulando o carregamento de dados
    data = pd.DataFrame({
        'Estudante': ['Ana', 'Bruno', 'Carla', 'Daniel', 'Eva'],
        'Dificuldade': ['Leitura', 'Matemática', 'Leitura', 'Escrita', 'Matemática'],
        'Nível': [3, 2, 4, 1, 5]
    })
    return data 
data = load_data()
st.subheader("Dados de Dificuldades de Aprendizagem")
st.dataframe(data)

st.subheader("Análise de Dificuldades")
difficulty_counts = data['Dificuldade'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=difficulty_counts.index, y=difficulty_counts.values, ax=ax)
ax.set_title("Contagem de Dificuldades por Tipo")
ax.set_xlabel("Tipo de Dificuldade")
ax.set_ylabel("Contagem")
st.pyplot(fig)

st.subheader("Nível de Dificuldade")
fig2, ax2 = plt.subplots()
sns.boxplot(x='Dificuldade', y='Nível', data=data, ax=ax2)
ax2.set_title("Nível de Dificuldade por Tipo")
ax2.set_xlabel("Tipo de Dificuldade")
ax2.set_ylabel("Nível")
st.pyplot(fig2)

st.markdown("""
### Conclusão
O SIDA é uma ferramenta valiosa para identificar e analisar dificuldades de aprendizagem, permitindo que educadores tomem decisões informadas para apoiar seus estudantes.
""")

st.markdown("2025 Sistema de Identificação de Dificuldades de Aprendizagem")
# Rodapé
st.markdown("""
<style>
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

