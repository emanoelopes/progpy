import tempfile

arq = tempfile.TemporaryFile()

print("Arquivo criado:", arq)

print("Nome do arquivo:", arq.name)
arq.close
