import numpy as np
from scipy.optimize import minimize_scalar

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
    return c + (1 - c) * (1 / (1 + np.exp(-a * (theta - b))))

def calcular_verossimilhanca(theta, a, b, c, x):
    # theta: valor da proficiência do candidato
    # a, b, c: parâmetros dos itens
    # x: matriz de respostas dos candidatos (0 para erro e 1 para acerto)
    if x.ndim == 1:
        x = np.expand_dims(x, axis=1)
    num_itens, num_candidatos = x.shape
    verossimilhanca = np.ones(num_candidatos)
    for i in range(num_itens):
        p = calcular_probabilidade(theta, a[i], b[i], c[i])
        verossimilhanca *= np.power(p, x[i]) * np.power(1-p, 1-x[i])
    return np.prod(verossimilhanca)

# Define a função de verossimilhança como uma função de theta
def verossimilhanca(theta, a, b, c, x):
    return -calcular_verossimilhanca(theta, a, b, c, x.flatten())  # O sinal negativo é usado porque o objetivo é maximizar a função

# Define os parâmetros dos itens e a matriz de respostas dos candidatos
a = [2.53465, 2.5914, 1.41618]
b = [2.4095, 1.40589, 0.30941]
c = [0.0954, 0.13998, 0.07884]
x = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]])

# Encontra o valor de theta que maximiza a função de verossimilhança para cada candidato usando o método de Brent
theta_max_list = []
for i in range(x.shape[1]):
    result = minimize_scalar(verossimilhanca, args=(a, b, c, x[:, i]), bounds=(-4, 5), method='bounded')
    theta_max_list.append((result.x*100)+500)

print(f"Valores de theta que maximizam a função de verossimilhança para cada candidato: {theta_max_list}")
