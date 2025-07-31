# This script identifies and extracts cursistas with errors from the AVA registration report.

import pandas as pd

# Define file paths (update these paths if your files are located elsewhere)
cursistas_file = '/content/Cursistas_Turma_A.xlsx'
ava_report_file = '/content/TurmaA-filename.csv'

# Define matching and display columns
matching_column_cursistas = '[0] login'
matching_column_ava = 'Login do Membro'
display_columns = ['Nome do Membro', 'Email do Membro', 'Login do Membro', '[3]CPF']


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

# Merge with df_cursistas to get CPF information using the cleaned login columns
errored_cursistas_with_cpf = pd.merge(
    errored_cursistas_df,
    df_cursistas[[matching_column_cursistas, '[3]CPF']], # Select cleaned login and CPF from df_cursistas
    how='left',
    left_on=matching_column_ava, # Use cleaned login from df_ava
    right_on=matching_column_cursistas # Use cleaned login from df_cursistas
)

# Select the desired columns including CPF
errored_cursistas_info_df = errored_cursistas_with_cpf[display_columns]

# Display the resulting DataFrame
print("Cursistas com 'Sim' na coluna 'Erro Apresentado?' (incluindo CPF):")
print(errored_cursistas_info_df.to_string())

# Optionally, save the result to a new Excel file
# errored_cursistas_info_df.to_excel('cursistas_com_erro.xlsx', index=False)
# print("\nArquivo 'cursistas_com_erro.xlsx' gerado com sucesso!")