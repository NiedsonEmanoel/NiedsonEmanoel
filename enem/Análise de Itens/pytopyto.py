import numpy as np
from scipy.optimize import minimize_scalar

def calculate_likelihood(theta, a, b, c, x):
    # theta: valor da proficiência do candidato
    # a, b, c: parâmetros dos itens
    # x: matriz de respostas dos candidatos (0 para erro e 1 para acerto)
    
    num_items, num_candidates = x.shape
    likelihood = np.ones(num_candidates)
    
    for i in range(num_items):
        p = c[i] + (1 - c[i]) / (1 + np.exp(-a[i] * (theta - b[i])))
        likelihood *= np.power(p, x[i, :]) * np.power(1 - p, 1 - x[i, :])
        
    return np.prod(likelihood)

# Define a função de verossimilhança como uma função de theta
def likelihood(theta, a, b, c, x):
    return -calculate_likelihood(theta, a, b, c, x)  # O sinal negativo é usado porque o objetivo é maximizar a função

# Define os parâmetros dos itens e a matriz de respostas dos candidatos
a = [1.0, 1.5, 2.0]
b = [-1.0, 0.0, 1.0]
c = [0.1, 0.2, 0.3]
x = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]])

# Encontra o valor de theta que maximiza a função de verossimilhança usando o método de Brent
result = minimize_scalar(likelihood, args=(a, b, c, x), bounds=(-10.0, 10.0), method='bounded')
theta_max = ((result.x*100)+500)

print(f"Valor de theta que maximiza a função de verossimilhança: {theta_max}")