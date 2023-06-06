import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
Disciplina = 'MT'

dItens = pd.read_csv('Simulados/simulado'+Disciplina+'.csv', encoding='utf-8', decimal=',')

def calcular_probabilidade(theta, a, b, c):
    """
    Calcula a probabilidade de uma resposta correta dado o nível de proficiência de um candidato e os parâmetros do item.

    Parâmetros:
        theta (float): Nível de proficiência do candidato.
        a (float): Parâmetro de discriminação.
        b (float): Parâmetro de dificuldade.
        c (float): Parâmetro de acerto ao acaso.

    Retorna:
        Probabilidade de uma resposta correta.
    """
    return c + (1 - c) / (1 + np.exp(-a * (theta - b)))

def calcular_verossimilhanca(theta, a, b, c, x):
    if x.ndim == 1:
        x = np.expand_dims(x, axis=1)
    num_itens, num_candidatos = x.shape
    verossimilhanca = np.ones(num_candidatos)
    for i, item in enumerate(x):
        p = calcular_probabilidade(theta, a[i], b[i], c[i])
        verossimilhanca *= np.power(p, item) * np.power(1 - p, 1 - item)
    return np.prod(verossimilhanca)

def encontrar_theta_max(a, b, c, x):
    if len(a) != x.shape[0] or len(b) != x.shape[0] or len(c) != x.shape[0]:
        raise ValueError("O comprimento das listas de parâmetros a, b e c deve corresponder ao número de itens em x.")

    if x.ndim == 1:
        x = np.expand_dims(x, axis=1)

    theta_max_list = []
    for i in range(x.shape[1]):
        result = minimize_scalar(lambda theta: -calcular_verossimilhanca(theta, a, b, c, x[:, i]), bounds=(-3, 5), method='bounded')
        theta_max_list.append(result.x * 100 + 500)
    return theta_max_list

# Define os parâmetros dos itens e a matriz de respostas dos candidatos
a, b, c = zip(*dItens[['NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']].values.tolist())

total = len(a)

x = np.ones(total)  # Initializing x with all 1s

i = 0
acertos = 0
while i < total:
    resposta = input("Digite a resposta da questão " + str(dItens.loc[i, 'CO_POSICAO']) + ": ")
    resposta = resposta.upper()  # Converter a resposta para letras maiúsculas
    
    gabarito = dItens.loc[i, 'TX_GABARITO']
    gabarito = gabarito.upper()  # Converter o gabarito para letras maiúsculas
    
    if resposta in ['A', 'B', 'C', 'D', 'E', 'X'] and len(resposta) == 1:
        if resposta == gabarito:
            x[i] = 1  # Atribuir 1 para acerto
            acertos +=1
        else:
            x[i] = 0  # Atribuir 0 para erro
        i += 1
    else:
        print("Resposta inválida. Digite apenas as letras A, B, C, D, E ou X.")
        
# Encontra o valor de theta que maximiza a função de verossimilhança para o candidato
try:
    theta_max_list = encontrar_theta_max(a, b, c, x)
    print(f"Nota TRI: {theta_max_list[0]}")
    print(f'Acertos: {acertos}')
except ValueError as e:
    print(f"Erro: {str(e)}")
