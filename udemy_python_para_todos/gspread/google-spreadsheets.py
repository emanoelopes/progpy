import gspread
import pandas as pd

gc = gspread.service_account()
sh = gc.open("Atividades do técnico de laboratório")
aba = sh.worksheet("Página1")
dados = aba.get_all_records()
df = pd.DataFrame(dados)
print(df)
