import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from PIL import Image

Disciplina = 'LC'
proficiencia_inicial = 670

dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
dItens = dItens[dItens['SG_AREA'] == Disciplina]
dItens = dItens.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

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

def jogo_proficiencia(df):
    proficiencia_atual = proficiencia_inicial
    pd_resultado = pd.DataFrame(columns=['NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'Theta065', 'Acerto'])

    for _ in range(15):
        questoes_disponiveis = df[df['theta_065'] == proficiencia_atual]
        if questoes_disponiveis.empty:
            questao = df.loc[df['theta_065'].sub(proficiencia_atual).abs().idxmin()]
        else:
            questao = questoes_disponiveis.sample(n=1).iloc[0]

        caminho_imagem = '../1. Itens BNI/' + str(questao['CO_ITEM']) + '.png'
        gabarito = questao['TX_GABARITO']

        imagem = Image.open(caminho_imagem)
        imagem.show()

        resposta = input("Digite a resposta (A, B, C, D ou E): ").upper()

        if resposta == gabarito:
            proficiencia_atual += 50
            acerto = 1
        else:
            acerto = 0

        pd_resultado = pd_resultado.append({
            'NU_PARAM_A': questao['NU_PARAM_A'],
            'NU_PARAM_B': questao['NU_PARAM_B'],
            'NU_PARAM_C': questao['NU_PARAM_C'],
            'Theta065': questao['theta_065'],
            'Acerto': acerto
        }, ignore_index=True)

        df = df.drop(questao.name)

        if len(pd_resultado) >= 2 and pd_resultado.iloc[-1]['Acerto'] == 0 and pd_resultado.iloc[-2]['Acerto'] == 0:
            proficiencia_atual -= 50

    return pd_resultado

resultado = jogo_proficiencia(dItens)

a, b, c, x = zip(*resultado[['NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'Acerto']].values.tolist())

print(resultado)

a = np.array(a)
b = np.array(b)
c = np.array(c)
x = np.array(x)

try:
    theta_max_list = encontrar_theta_max(a, b, c, x)
    print(f"Nota TRI (estimada): {theta_max_list[0]:.2f}")
    print(f'Acertos: {np.sum(x)}/15')
except ValueError as e:
    print(f"Erro: {str(e)}")
