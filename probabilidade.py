import pandas as pd

# Caminho do arquivo na pasta sample_data
file_path = 'DO23OPEN.csv'

# Carregar o arquivo CSV usando o delimitador ponto-e-vírgula
data = pd.read_csv(file_path, delimiter=';')

# Mapear os valores do campo SEXO
sexo_map = {1: 'Masculino', 2: 'Feminino', 9: 'Ignorado'}
data['SEXO'] = data['SEXO'].map(sexo_map)

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

# 1. Probabilidade de Falecer de Infarto Agudo do Miocárdio (I219) Dado que é Homem
total_homens = data['SEXO'].value_counts().get('Masculino', 0)
homens_i219 = data[(data['SEXO'] == 'Masculino') & (data['CAUSABAS'] == 'I219')].shape[0]
prob_i219_homem = homens_i219 / total_homens
print(f"Probabilidade de falecer de Infarto Agudo do Miocárdio (I219) dado que é homem: {prob_i219_homem:.4f}")

# 2. Probabilidade de uma Causa Específica de Morte Dado o Sexo
# Definir as causas específicas de morte que queremos analisar
causas_especificas = ['I219', 'J189', 'I10', 'C61', 'C349']

for causa in causas_especificas:
    total_mulheres = data['SEXO'].value_counts().get('Feminino', 0)
    mulheres_causa = data[(data['SEXO'] == 'Feminino') & (data['CAUSABAS'] == causa)].shape[0]
    prob_causa_mulher = mulheres_causa / total_mulheres
    
    total_homens = data['SEXO'].value_counts().get('Masculino', 0)
    homens_causa = data[(data['SEXO'] == 'Masculino') & (data['CAUSABAS'] == causa)].shape[0]
    prob_causa_homem = homens_causa / total_homens
    
    print(f"Probabilidade de falecer de {causa} dado que é mulher: {prob_causa_mulher:.4f}")
    print(f"Probabilidade de falecer de {causa} dado que é homem: {prob_causa_homem:.4f}")

# 3. Probabilidade de uma Pessoa de 60 Anos ou Mais Falecer de Pneumonia (J189)
total_60_anos_ou_mais = data[data['IDADE_ANOS'] >= 60].shape[0]
pneumonia_60_anos_ou_mais = data[(data['IDADE_ANOS'] >= 60) & (data['CAUSABAS'] == 'J189')].shape[0]
prob_j189_60_anos_ou_mais = pneumonia_60_anos_ou_mais / total_60_anos_ou_mais
print(f"Probabilidade de uma pessoa de 60 anos ou mais falecer de Pneumonia (J189): {prob_j189_60_anos_ou_mais:.4f}")
