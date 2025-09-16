import streamlit as st
from transformers import pipeline

st.title("Um App Simples de Análise de Sentimentos com Hugging Face Transformers")
text = st.text_area("Por favor, escreva sua sentença.")
model = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", top_k=None)
if st.button("Análise de Sentimentos"):
    if len(text) <= 1:
        result = "Por favor, forneça uma sentença."
    else:
        res = model(text)
        result = f"A sentença é {round(res[0][0]['score']*100, 2)}% {res[0][0]['label']}, {round(res[0][1]['score']*100, 2)}% {res[0][1]['label']} e {round(res[0][2]['score']*100, 2)}% {res[0][2]['label']}."
        result = result.replace("positive", "positiva")
        result = result.replace("negative", "negativa")
        result = result.replace("neutral", "neutra")
    st.write(result)