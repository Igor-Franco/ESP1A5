import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo na pasta sample_data
file_path = 'DO23OPEN.csv'  

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';')

# Função para calcular a idade em anos a partir do campo "IDADE"
def calcular_idade_em_anos(idade):
    if pd.isnull(idade):
        return None
    str_idade = str(int(idade)).zfill(3)
    unidade = int(str_idade[0])
    quantidade = int(str_idade[1:])

    if unidade == 1:  # Minutos
        anos = quantidade / (60 * 24 * 365.25)
    elif unidade == 2:  # Horas
        anos = quantidade / (24 * 365.25)
    elif unidade == 3:  # Meses
        anos = quantidade / 12
    elif unidade == 4:  # Anos
        anos = quantidade
    elif unidade == 5:  # Idade maior que 100 anos
        anos = 100 + quantidade
    else:
        anos = None

    return anos

# Aplicar a função para calcular a idade
data['IDADE_ANOS'] = data['IDADE'].apply(calcular_idade_em_anos)

# Remover valores nulos de idade calculada
data = data.dropna(subset=['IDADE_ANOS'])

# Calcular a média da idade
media_idade = data['IDADE_ANOS'].mean()
print(f"Média da idade: {media_idade:.2f} anos")

# Calcular a mediana da idade
mediana_idade = data['IDADE_ANOS'].median()
print(f"Mediana da idade: {mediana_idade:.2f} anos")

# Calcular o desvio padrão da idade
desvio_padrao_idade = data['IDADE_ANOS'].std()
print(f"Desvio padrão da idade: {desvio_padrao_idade:.2f} anos")

# Calcular a variância da idade
variancia_idade = data['IDADE_ANOS'].var()
print(f"Variância da idade: {variancia_idade:.2f} anos")

# Calcular e imprimir valores mínimos e máximos da idade
idade_min = data['IDADE_ANOS'].min()
idade_max = data['IDADE_ANOS'].max()
print(f"Idade mínima: {idade_min:.2f} anos")
print(f"Idade máxima: {idade_max:.2f} anos")

# Gerar histograma da idade com intervalos de 10 anos
plt.figure(figsize=(10, 5))
plt.hist(data['IDADE_ANOS'], bins=range(0, 110, 10), edgecolor='black')
plt.xlabel('Idade')
plt.ylabel('Frequência')
plt.title('Histograma da Idade')
plt.xticks(range(0, 110, 10))
plt.grid(axis='y')
plt.show()

# Gerar boxplot da idade
plt.figure(figsize=(10, 5))
plt.boxplot(data['IDADE_ANOS'], vert=False)
plt.xlabel('Idade')
plt.title('Boxplot da Idade')
plt.grid(axis='x')
plt.show()
