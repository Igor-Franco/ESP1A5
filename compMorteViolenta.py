import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo na pasta sample_data
file_path = 'DO23OPEN.csv'

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';')

# Mapear os valores do campo SEXO
sexo_map = {1: 'Masculino', 2: 'Feminino', 9: 'Ignorado'}
data['SEXO'] = data['SEXO'].map(sexo_map)

# Mapear os valores do campo CIRCOBITO
circobito_map = {1: 'Acidente', 2: 'Suicídio', 3: 'Homicídio', 4: 'Outros', 9: 'Ignorado'}
data['CIRCOBITO'] = data['CIRCOBITO'].map(circobito_map)

# Criar a tabela de contingência para CIRCOBITO por SEXO
tabela_circobito_sexo = pd.crosstab(data['CIRCOBITO'], data['SEXO'])

# Imprimir os valores absolutos
print("Valores absolutos das mortes violentas (CIRCOBITO) por sexo:")
print(tabela_circobito_sexo)

# Criar a tabela comparativa
tabela_comparativa = tabela_circobito_sexo.reset_index()

# Cores para o gráfico
cores = [ '#ff69b4','#1f77b4', '#d3d3d3']  # Azul para homens, rosa para mulheres, cinza para ignorado

# Gerar gráfico de barras lado a lado para cada tipo de morte violenta
tabela_circobito_sexo.plot(kind='bar', figsize=(10, 6), edgecolor='black', color=cores)
plt.title('Distribuição de Mortes Violentas por Sexo')
plt.xlabel('Tipo de Morte Violenta')
plt.ylabel('Número de Casos')
plt.legend(title='Sexo')
plt.grid(axis='y')
plt.xticks(rotation=0)
plt.show()

