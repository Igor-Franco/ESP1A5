import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, shapiro, kstest, probplot

# Caminho do arquivo CSV no diretório local
file_path = 'DO23OPEN.csv'

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';', low_memory=False)

# Mapear os valores do campo SEXO
sexo_map = {1: 'Masculino', 2: 'Feminino', 9: 'Ignorado'}
data['SEXO'] = data['SEXO'].map(sexo_map)

# Função para calcular a idade em anos a partir do campo "IDADE"
def calcular_idade_em_anos(idade):
    if pd.isna(idade):
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

# Calcular a média e o desvio padrão da idade
mean_age = data['IDADE_ANOS'].mean()
std_age = data['IDADE_ANOS'].std()

print(f"Média da Idade: {mean_age}")
print(f"Desvio Padrão da Idade: {std_age}")

# 1. Histograma com Curva de Densidade
idade_range = np.linspace(data['IDADE_ANOS'].min(), data['IDADE_ANOS'].max(), 1000)
normal_dist = norm.pdf(idade_range, mean_age, std_age)

plt.figure(figsize=(10, 6))
plt.hist(data['IDADE_ANOS'], bins=30, density=True, alpha=0.6, color='g', label='Histograma das Idades')
plt.plot(idade_range, normal_dist, label='Distribuição Normal', color='red')
plt.xlabel('Idade')
plt.ylabel('Densidade')
plt.title('Distribuição Normal da Idade dos Óbitos')
plt.legend()
plt.grid(True)
plt.show()

# 2. Gráfico Q-Q
plt.figure(figsize=(10, 6))
probplot(data['IDADE_ANOS'], dist="norm", plot=plt)
plt.title('Gráfico Q-Q da Idade dos Óbitos')
plt.grid(True)
plt.show()

# 3. Testes de Normalidade

# Teste de Shapiro-Wilk
shapiro_stat, shapiro_p_value = shapiro(data['IDADE_ANOS'])
print(f"Teste de Shapiro-Wilk: estatística={shapiro_stat}, p-valor={shapiro_p_value}")

# Teste de Kolmogorov-Smirnov
ks_stat, ks_p_value = kstest(data['IDADE_ANOS'], 'norm', args=(mean_age, std_age))
print(f"Teste de Kolmogorov-Smirnov: estatística={ks_stat}, p-valor={ks_p_value}")
