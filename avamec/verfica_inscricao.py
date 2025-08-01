# This script identifies and extracts cursistas with errors from the AVA registration report.

import pandas as pd

# Define file paths (update these paths if your files are located elsewhere)
cursistas_file = '/content/Cursistas Turma_A.xlsx'
ava_report_file = '/content/grp4_sec3_turmaA.csv'

# Define matching columns
matching_column_cursistas = '[0] login'
matching_column_ava = 'Login do Membro'

# Load the dataframes
try:
    df_cursistas = pd.read_excel(cursistas_file)
    df_ava = pd.read_csv(ava_report_file)
except FileNotFoundError as e:
    print(f"Error loading file: {e}. Make sure the file paths are correct.")
    exit()

# Clean the matching columns
df_cursistas[matching_column_cursistas] = df_cursistas[matching_column_cursistas].astype(str).str.strip().str.lower()
df_ava[matching_column_ava] = df_ava[matching_column_ava].astype(str).str.strip().str.lower()

# Filter rows where 'Erro Apresentado?' is 'Sim'
errored_cursistas_df = df_ava[df_ava['Erro Apresentado?'] == 'Sim'].copy() # Use .copy() to avoid SettingWithCopyWarning

# Merge with the entire df_cursistas dataframe using the cleaned login columns
errored_cursistas_with_cursistas_info = pd.merge(
    errored_cursistas_df,
    df_cursistas,
    how='left',
    left_on=matching_column_ava, # Use cleaned login from df_ava
    right_on=matching_column_cursistas # Use cleaned login from df_cursistas
)

# Replace the values in the '[0] login' column with values from 'Login existente' where available
errored_cursistas_with_cursistas_info[matching_column_cursistas] = errored_cursistas_with_cursistas_info['Login existente'].fillna(errored_cursistas_with_cursistas_info[matching_column_cursistas])


# Select only the columns that are present in df_cursistas and maintain their original order
final_errored_cursistas_df = errored_cursistas_with_cursistas_info[df_cursistas.columns]

# Display the resulting DataFrame
print("Cursistas com 'Sim' na coluna 'Erro Apresentado?' (com colunas na ordem do df_cursistas):")
print(final_errored_cursistas_df.to_string())

# Save the result to a new Excel file
final_errored_cursistas_df.to_excel('cursistas_com_erro_completo.xlsx', index=False)
print("\nArquivo 'cursistas_com_erro_completo.xlsx' gerado com sucesso e pronto para importação no AVAMEC!")