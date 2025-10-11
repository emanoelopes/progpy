import streamlit as st
from  import ChatOllama

llm = ChatOllama(model="qwen2.5-coder:7b", base_url="http://localhost:11434")

st.set_page_config(page_title="Chat with Qwen", page_icon=":robot:", layout="centered")
st.title("Converse com DeepSeek")

prompt = st.chat_input("Digite sua mensagem:")
if prompt:
    st.chat_message("human").markdown(prompt)
    resposta = llm.invoke(prompt)
    st.chat_message("ia").markdown(resposta.content)