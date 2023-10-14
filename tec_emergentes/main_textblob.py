from textblob import TextBlob
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob.sentiments import NaiveBayesAnalyzer


# Função para realizar a análise de sentimento
def analisar_sentimento_TextBlob(texto):
# Criar um objeto TextBlob com o texto de entrada
  tb = TextBlob(texto)
  # Traduzir o texto para o inglês (TextBlob funciona melhor em inglês)
  tb = tb.translate(from_lang='pt', to='en')
  # Calcular a polaridade (de -1 a 1, onde -1 é negativo, 0 é neutro e 1 é positivo)
  polaridade = tb.sentiment.polarity
  if polaridade > 0:
    return "Positivo"
  elif polaridade < 0:
    return "Negativo"
  else:
    return "Neutro"


# Baixe os recursos necessários (caso ainda não tenha feito isso)
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
# Função para realizar a análise de sentimento
def analisar_sentimento_vader(texto):
  # Inicialize o SentimentIntensityAnalyzer
  sia = SentimentIntensityAnalyzer()
  # Obtenha a polaridade do sentimento
  sentiment = sia.polarity_scores(texto)
  # Determine o sentimento com base na polaridade
  if sentiment['compound'] >= 0.05:
    return "Positivo"
  elif sentiment['compound'] <= -0.05:
    return "Negativo"
  else:
    return "Neutro"
# Exemplo de uso
"""
Análise de sentimentos de conversas extraídas de um grupo de condomínio.
"""
frases = []
with open("../../palmeiras.txt", encoding="utf-8") as arq:
    for lin in arq:
        frases += lin.splitlines()
df = pd.DataFrame(columns = ['linha', 'Polaridade', 'Subjetividade', 'Classificação'])
blob = TextBlob("".join(frases), analyzer=NaiveBayesAnalyzer())
for frase in blob.sentences:
    df.loc[len(df)] = [str(frase),frase.polarity, frase.subjectivity, frase.sentiment]
print(df)
#print(df.loc[[10]])
stm = analisar_sentimento_vader(frases)
print("[vader]O grupo do condomínio é: " + str(stm))
stm = analisar_sentimento_TextBlob(frases)
print("[TextBlob]O Grupo do condomínio é: " + str(stm))

mensagem = input("Digite uma mensagem: ")
sentimento = analisar_sentimento_vader(mensagem)
print("[vader]A mensagem é: " + str(sentimento))
sentimento = analisar_sentimento_TextBlob(mensagem)
print("[TextBlob]A mensagem é: " + str(sentimento))
