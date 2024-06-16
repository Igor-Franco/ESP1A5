import pandas as pd

# Caminho do arquivo na pasta sample_data
file_path = 'DO23OPEN.csv'

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';')

# Obter o número de linhas e colunas
num_linhas, num_colunas = data.shape
print(f"O arquivo CSV tem {num_linhas} linhas e {num_colunas} colunas.")

# Imprimir os nomes das colunas
print("Nomes das colunas:", data.columns)
