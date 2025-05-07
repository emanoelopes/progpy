from flask import Flask, render_template, request
import pandas as pd
from io import StringIO

app = Flask(__name__)

def merge_datasets(file1_content, file2_content, merge_column, how):
    """
    Merges two datasets based on a common column and merge type.

    Args:
        file1_content (str): Content of the first dataset (CSV format).
        file2_content (str): Content of the second dataset (CSV format).
        merge_column (str): Name of the column to merge on.
        how (str): Type of merge ('inner', 'outer', 'left', 'right').

    Returns:
        str: Merged dataset in CSV format, or an error message.
    """
    try:
        df1 = pd.read_csv(StringIO(file1_content))
        df2 = pd.read_csv(StringIO(file2_content))

        if merge_column not in df1.columns or merge_column not in df2.columns:
            return "Erro: A coluna de merge especificada não existe em um ou ambos os datasets."

        merged_df = pd.merge(df1, df2, on=merge_column, how=how)
        return merged_df.to_csv(index=False)
    except Exception as e:
        return f"Erro ao processar os arquivos: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file1' not in request.files or 'file2' not in request.files:
            return render_template('index.html', error="Erro: Por favor, selecione os dois arquivos.")

        file1 = request.files['file1']
        file2 = request.files['file2']
        merge_column = request.form['merge_column']
        how = request.form['merge_type']

        if file1.filename == '' or file2.filename == '':
            return render_template('index.html', error="Erro: Por favor, selecione os dois arquivos.")

        if file1 and file2:
            file1_content = file1.stream.read().decode('utf-8')
            file2_content = file2.stream.read().decode('utf-8')
            merged_data = merge_datasets(file1_content, file2_content, merge_column, how)
            if merged_data.startswith("Erro"):
                return render_template('index.html', error=merged_data)
            else:
                return render_template('result.html', merged_data=merged_data)

    return render_template('index.html', error=None)

@app.route('/result')
def result():
    merged_data = request.args.get('merged_data')
    return render_template('result.html', merged_data=merged_data)

if __name__ == '__main__':
    app.run(debug=True)