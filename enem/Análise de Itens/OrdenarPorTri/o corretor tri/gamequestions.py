Disciplina = input("Digite a sigla da disciplina desejada: MT, LC, CH, CN: ").upper()
proficiencia_inicial = ((float(input("Digite a proficiência inicial: "))+500)/2)

import numpy as np
import pandas as pd
from PIL import Image
import pygame
import sys
import os
from scipy.optimize import minimize_scalar
qtdQuestoes = 25


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

def show_image(image_path, zoom):
    pygame.init()
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    original_image = Image.open(image_path)
    image_width, image_height = original_image.size
    scaled_image = original_image.resize((int(image_width * zoom), int(image_height * zoom)))
    image = pygame.image.fromstring(scaled_image.tobytes(), scaled_image.size, scaled_image.mode)
    image_rect = image.get_rect(center=screen.get_rect().center)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    resposta = 'A'
                    running = False
                elif event.key == pygame.K_b:
                    resposta = 'B'
                    running = False
                elif event.key == pygame.K_c:
                    resposta = 'C'
                    running = False
                elif event.key == pygame.K_d:
                    resposta = 'D'
                    running = False
                elif event.key == pygame.K_e:
                    resposta = 'E'
                    running = False
                elif event.key == pygame.K_x:
                    resposta = 'X'
                    running = False
                elif event.key == pygame.K_KP_PLUS or (event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_CTRL):
                    zoom += 0.1
                    scaled_image = original_image.resize((int(image_width * zoom), int(image_height * zoom)))
                    image = pygame.image.fromstring(scaled_image.tobytes(), scaled_image.size, scaled_image.mode)
                    image_rect = image.get_rect(center=screen.get_rect().center)
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    zoom -= 0.1
                    if zoom < 0.1:
                        zoom = 0.1
                    scaled_image = original_image.resize((int(image_width * zoom), int(image_height * zoom)))
                    image = pygame.image.fromstring(scaled_image.tobytes(), scaled_image.size, scaled_image.mode)
                    image_rect = image.get_rect(center=screen.get_rect().center)

        screen.fill((255, 255, 255))
        screen.blit(image, image_rect)
        pygame.display.flip()
        clock.tick(60)

    return resposta

def show_results(results, triString):
    pygame.init()
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 50)
    text_color = (0, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))

        rendered_textTRI = font.render(triString, True, text_color)
        screen.blit(rendered_textTRI, (screen_width/3, 50))

        pygame.display.flip()
        clock.tick(60)

def jogo_proficiencia(df):
    proficiencia_atual = proficiencia_inicial
    pd_resultado = pd.DataFrame(columns=['CO_HABILIDADE','NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'Theta065', 'Acerto'])

    for _ in range(qtdQuestoes):
        questoes_disponiveis = df[df['theta_065'] == proficiencia_atual]
        if questoes_disponiveis.empty:
            questao = df.loc[df['theta_065'].sub(proficiencia_atual).abs().idxmin()]
        else:
            questao = questoes_disponiveis.sample(n=1).iloc[0]

        caminho_imagem = '../1. Itens BNI/' + str(questao['CO_ITEM']) + '.png'
        gabarito = questao['TX_GABARITO']

        resposta = show_image(caminho_imagem, 1.0).upper()

        if resposta == gabarito:
            proficiencia_atual += 50
            acerto = 1
        else:
            acerto = 0

        pd_resultado = pd_resultado.append({
            'CO_HABILIDADE': questao['CO_HABILIDADE'],
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

del resultado['NU_PARAM_A']
del resultado['NU_PARAM_B']
del resultado['NU_PARAM_C']

strResu = str(resultado)

a = np.array(a)
b = np.array(b)
c = np.array(c)
x = np.array(x)

strTri = ""

try:
    theta_max_list = encontrar_theta_max(a, b, c, x)
    strTri = (f"Nota TRI (estimada): {theta_max_list[0]:.2f} - Acertos: {np.sum(x)}/{qtdQuestoes}")
except ValueError as e:
    strTri = (f"Erro: {str(e)}")

os.system('cls')

print(strTri)
print('\n')
print(strResu)
print('\n')


show_results(strResu, strTri)

#GERAR PDF COM CERTAS E ERRADAS E ENVIAR POR EMAIL