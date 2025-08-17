import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import SystemMessage
# from google.colab import userdata # Remove this import

# Load API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()


# Load PDF and create vectorstore
loader = PyPDFLoader("/home/demo/Downloads/guia_do_att.pdf") # This path might need adjustment for local execution
documents = loader.load()
embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=GOOGLE_API_KEY)
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# Initialize chat model and system message
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=GOOGLE_API_KEY)
system_message = SystemMessage(content='''
Você é um assistente especializado no atendimento ao usuário do PRODITEC. Responda claramente a perguntas sobre procedimentos do AVAMEC. Se a pergunta nao estiver contida no ducmento, responda: Favor entrar em contato com o suporte.
''')

# Setup session history
store = {}
def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Create conversational retrieval chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm = chat,
    retriever = retriever,
    return_source_documents = False
    )

chain_with_history = RunnableWithMessageHistory(
    runnable = qa_chain,
    get_session_history = get_session_history,
    input_messages_key='question',
    output_messages_key='answer',
    history_messages_key='chat_history'
)

# Streamlit application setup
st.set_page_config(page_title="PRODITEC Assistant", page_icon=":books:")

st.write(system_message.content)

# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if question := st.chat_input("Digite sua pergunta:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question)

    # Invoke the chain with history
    session_id = "streamlit_session" # Using a fixed session ID for simplicity in this example
    response = chain_with_history.invoke(
        {'question': question},
        config={'configurable': {'session_id': session_id}}
    )

    # Add AI message to chat history
    ai_response = response['answer']
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(ai_response)