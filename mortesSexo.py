import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo na pasta sample_data
file_path = 'DO23OPEN.csv'

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';')

# Mapear os valores do campo SEXO
sexo_map = {1: 'Masculino', 2: 'Feminino', 9: 'Ignorado'}
data['SEXO'] = data['SEXO'].map(sexo_map)

# Nome da coluna para a causa de óbito
causa_obito_coluna = 'CAUSABAS'

# Função para agrupar as causas de óbito
def agrupar_causas(data, causa_obito_coluna, sexo, top_n=10):
    causas_sexo = data[data['SEXO'] == sexo][causa_obito_coluna].value_counts()
    principais_causas = causas_sexo.head(top_n)
    restantes_causas = pd.Series({'Outros': causas_sexo[top_n:].sum()})

    causas_agrupadas = pd.concat([principais_causas, restantes_causas])
    return causas_agrupadas

# Definir uma paleta de cores personalizada
cores_personalizadas = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f', '#76d7c4', '#e59866', '#d0ece7', '#f7f9f9']

# Gerar gráficos de pizza para cada sexo
for sexo in ['Masculino', 'Feminino']:
    causas_agrupadas = agrupar_causas(data, causa_obito_coluna, sexo)

    # Imprimir valores absolutos das 10 principais causas de óbito
    print(f"\nValores absolutos das 10 principais causas de óbito para {sexo}:")
    print(causas_agrupadas)

    plt.figure(figsize=(8, 8))
    plt.pie(causas_agrupadas, labels=causas_agrupadas.index, autopct='%1.1f%%', startangle=140, colors=cores_personalizadas[:len(causas_agrupadas)])
    plt.title(f'Distribuição das 10 Principais Causas de Óbito para {sexo}')
    plt.axis('equal')  # Garantir que o gráfico seja um círculo
    plt.show()

