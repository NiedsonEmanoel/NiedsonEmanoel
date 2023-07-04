import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
Disciplina = 'mt'.upper()
Habilidade = 4

dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')

dItens = dItens[dItens['SG_AREA'] == Disciplina]
dItens = dItens[dItens['IN_ITEM_ABAN'] == 0]
dItens = dItens[dItens['CO_HABILIDADE'] == Habilidade]
dItens.sort_values('theta_065', ascending=True, inplace=True)
dItens['indexacao'] = dItens.reset_index().index + 1

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
while i < total:
    answer = input("Digite 1 ou 0 como resposta da questão "+(str(i+1))+": ")
    if answer == "1":
        x[i] = 1
        i += 1
    elif answer == "0":
        x[i] = 0
        i += 1
    else:
        print("Resposta inválida. Digite apenas 1 ou 0.")

# Encontra o valor de theta que maximiza a função de verossimilhança para o candidato
try:
    theta_max_list = encontrar_theta_max(a, b, c, x)
    print(f"Nota TRI H{Habilidade} - {Disciplina}: {theta_max_list[0]}")
except ValueError as e:
    print(f"Erro: {str(e)}")
