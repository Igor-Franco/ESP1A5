import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo na pasta sample_data
file_path = 'DO23OPEN.csv'  # Note o nome corrigido do arquivo

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';')

# Mapear os valores do campo SEXO
sexo_map = {1: 'Masculino', 2: 'Feminino', 9: 'Ignorado'}
data['SEXO'] = data['SEXO'].map(sexo_map)

# Contar a quantidade de homens e mulheres
contagem_sexo = data['SEXO'].value_counts()

# Imprimir o número total de registros
total_registros = len(data)
print(f"Número total de registros: {total_registros}")

# Imprimir os valores absolutos
print("Contagem de mortes por sexo:")
print(contagem_sexo)

# Gerar gráfico de pizza
plt.figure(figsize=(8, 8))
plt.pie(contagem_sexo, labels=contagem_sexo.index, autopct='%1.1f%%', startangle=140, colors=['blue', 'pink', 'grey'])
plt.title('Distribuição de Mortes por Sexo')
plt.axis('equal')  # Garantir que o gráfico seja um círculo
plt.show()
