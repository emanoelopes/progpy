import streamlit as st
import pandas as pd

df = pd.read_csv('oulad_atributos_selecionados.csv')

df.head()
st.dataframe(df)