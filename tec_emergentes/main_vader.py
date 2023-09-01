import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Baixe os recursos necessários (caso ainda não tenha feito isso)
nltk.download('vader_lexicon')
# Função para realizar a análise de sentimento
def analisar_sentimento(texto):
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
mensagem = ""
sentimento = analisar_sentimento(mensagem)
print("A mensagem é: " + str(sentimento))
