import pandas as pd
import numpy as np
from scipy.stats import norm, shapiro, kstest, ttest_1samp, t

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

# Selecionar uma amostra aleatória dos dados
sample_size = 5000  # Tamanho da amostra
sample_data = data['IDADE_ANOS'].sample(sample_size, random_state=1)

# Calcular a média e o desvio padrão da amostra
mean_age_sample = sample_data.mean()
std_age_sample = sample_data.std()

print(f"Média da Idade (Amostra): {mean_age_sample}")
print(f"Desvio Padrão da Idade (Amostra): {std_age_sample}")

# Calcular o valor crítico para um intervalo de confiança de 95% usando a amostra
n = sample_size
grau_de_liberdade = n - 1
conf_interval = 0.95
alpha = 1 - conf_interval
t_critical = t.ppf(1 - alpha/2, df=grau_de_liberdade)

print(f"Valor crítico para um intervalo de confiança de 95%: {t_critical}")

# Intervalo de confiança usando a amostra
intervalo_confianca = t_critical * (std_age_sample / np.sqrt(n))

# Limites inferior e superior do intervalo de confiança
ic_inferior = mean_age_sample - intervalo_confianca
ic_superior = mean_age_sample + intervalo_confianca

print(f"Intervalo de Confiança de 95% para a média da idade (Amostra): [{ic_inferior}, {ic_superior}]")

# Testes de Normalidade usando a amostra

# Teste de Shapiro-Wilk
shapiro_stat, shapiro_p_value = shapiro(sample_data)
print(f"Teste de Shapiro-Wilk: estatística={shapiro_stat}, p-valor={shapiro_p_value}")

# Teste de Kolmogorov-Smirnov
ks_stat, ks_p_value = kstest(sample_data, 'norm', args=(mean_age_sample, std_age_sample))
print(f"Teste de Kolmogorov-Smirnov: estatística={ks_stat}, p-valor={ks_p_value}")

# Teste de Hipóteses usando a amostra
# Hipótese nula: A média das idades dos óbitos é 70 anos
# Hipótese alternativa: A média das idades dos óbitos não é 70 anos
media_hipotetica = 70
ttest_stat, ttest_p_value = ttest_1samp(sample_data, media_hipotetica)
print(f"Teste t para uma amostra: estatística={ttest_stat}, p-valor={ttest_p_value}")

# Verificar se rejeitamos a hipótese nula
if ttest_p_value < alpha:
    print("Rejeitamos a hipótese nula. A média das idades dos óbitos é significativamente diferente de 70 anos.")
else:
    print("Não rejeitamos a hipótese nula. Não há evidência suficiente para afirmar que a média das idades dos óbitos é diferente de 70 anos.")
