Disciplina = input("Digite a sigla da disciplina desejada: MT, LC, CH, CN: ").upper()
proficiencia_inicial = ((float(input("Digite a proficiência inicial: "))+500)/2)
qtdQuestoes = 25

import numpy as np
import pandas as pd
from PIL import Image
import pygame
import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from scipy.optimize import minimize_scalar
pd.options.mode.chained_assignment = None

dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
dItens = dItens[dItens['SG_AREA'] == Disciplina]
dItens = dItens.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

def toYoutube(textPrompt):
    search_query = "https://www.youtube.com/results?search_query=" + "+".join(textPrompt.split())
    return(search_query)

DisciplinaCompleto = ''
if Disciplina == 'MT':
    DisciplinaCompleto = 'Matemática'
if Disciplina == 'LC':
    DisciplinaCompleto = 'Linguagens'
if Disciplina == 'CH':
    DisciplinaCompleto = 'Humanas'
if Disciplina == 'CN':
    DisciplinaCompleto = 'Natureza'

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

#Definindo Classe do PDF de Saída
class PDF(FPDF):
    def header(self):
        self.image('../natureza/fundo.png', x=0, y=0, w=self.w, h=self.h, type='png')

    def add_my_link(self, x, y, txt, link):
        self.set_xy(x, y)
        self.set_text_color(0, 0, 0)
        self.set_font('Times', 'BI', 12)
        self.add_link()
        
        # obter a largura do texto
        w = self.get_string_width(txt) + 6  # adicione uma margem de 3 em cada lado
        
        # desenhar o retângulo em torno do texto
        self.set_fill_color(255, 112, 79)
        self.cell(w, 10, '', border=0, ln=0, fill=True, align='C', link=link)
        
        # adicionar o texto com o link
        self.set_xy(x, y)
        self.cell(w, 10, txt, border=0, ln=1, align='C', link=link)
        
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'BI', 8)
        # Page number
        self.cell(0, 12, 'Página ' + str(self.page_no()) + '/{nb}' + ' por @niedson.studiesmed', 0, 0, 'C')    

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
    pd_resultado = pd.DataFrame(columns=['TX_GABARITO', 'ANO', 'CO_PROVA', "CO_POSICAO", 'CO_HABILIDADE','NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'CO_ITEM', 'theta_065', 'Acerto'])

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
            'CO_PROVA': questao['CO_PROVA'],
            'CO_POSICAO': questao['CO_POSICAO'],
            'TX_GABARITO': questao['TX_GABARITO'],
            'CO_ITEM':questao['CO_ITEM'],
            'ANO': questao['ANO'],
            'CO_HABILIDADE': questao['CO_HABILIDADE'],
            'NU_PARAM_A': questao['NU_PARAM_A'],
            'NU_PARAM_B': questao['NU_PARAM_B'],
            'NU_PARAM_C': questao['NU_PARAM_C'],
            'theta_065': questao['theta_065'],
            'Acerto': acerto
        }, ignore_index=True)

        df = df.drop(questao.name)

        if len(pd_resultado) >= 2 and pd_resultado.iloc[-1]['Acerto'] == 0 and pd_resultado.iloc[-2]['Acerto'] == 0:
            proficiencia_atual -= 50

    return pd_resultado

def get_prova_string(ano, co_prova):
    if ano == 2016:
        if co_prova in [303]:
            return 'PROVA AZUL'
    if ano == 2018:
        if co_prova in [456, 452]:
            return 'PROVA AMARELA'
        elif co_prova in [449, 462]:
            return 'PROVA CINZA'
        elif co_prova in [496, 492]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    if ano == 2019:
        if co_prova in [512, 508]:
            return 'PROVA AMARELA'
        elif co_prova in [505, 518]:
            return 'PROVA CINZA'
        elif co_prova in [552, 548]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    elif ano == 2020:
        if co_prova in [578, 568]:
            return 'PROVA AMARELA'
        elif co_prova in [599, 590]:
            return 'PROVA CINZA'
        elif co_prova in [658, 648]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'
    else: #2021
        if co_prova in [890, 880]:
            return 'PROVA AMARELA'
        elif co_prova in [902, 911]:
            return 'PROVA CINZA'
        elif co_prova in [960, 970]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO' 

def enviar_email(receiver_email):

    subject = 'Questões Erradas de '+DisciplinaCompleto

    smtp_server='smtp.gmail.com'
    smtp_port=587
    smtp_username='smtp.niedson@gmail.com'
    smtp_password=''

    filename = 'erradas.pdf'

    body = 'Questões Erradas de '+DisciplinaCompleto

    # Criação da mensagem de email
    message = MIMEMultipart()
    sender_email = smtp_username
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Adiciona o corpo do email
    message.attach(MIMEText(body, 'plain'))

    # Anexa o arquivo PDF
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=filename)

    message.attach(part)

    # Conecta-se ao servidor SMTP e envia o email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print('Email enviado com sucesso!')
    except Exception as e:
        print('Ocorreu um erro ao enviar o email:', str(e))

#Função que gera a lista de Treino de TRI
def questionNow(dfResult):
    name = DisciplinaCompleto

    dfResult.sort_values('theta_065', ascending=True, inplace=True)
    dfResult['QSEARCH'] = dfResult.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)
    dfResult['indexacao'] = dfResult.reset_index().index + 1

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

    pdf.add_page()

    pdf.set_font('Times', 'B', 12)


    for i in dfResult.index:
        print("N"+str(dfResult.loc[i, 'indexacao'])+"/"+str(len(dfResult)))
        strCH = "N" + str(dfResult.loc[i, 'indexacao']) + " - Q" + str(dfResult.loc[i, "CO_POSICAO"]) + ':' + str(dfResult.loc[i, "ANO"]) + ' - H' + str(dfResult.loc[i, "CO_HABILIDADE"].astype(int)) + " - Proficiência: " + str(round(dfResult.loc[i, "theta_065"], 2))
        if 'dtype:' in strCH:
            print("CaCHulando...")
        else:
            try:
                # obter as dimensões da imagem
                with Image.open('../1. Itens BNI/' + str(dfResult.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size                
                pdf.set_fill_color(255, 112, 79) 
                pdf.ln(15)
                pdf.cell(0, 10, strCH, 0, 1, 'C', 1)
                pdf.ln(10)   # adicionar espaço entre o texto e a imagem

                # caCHular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('../1. Itens BNI/' + str(dfResult.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)
                pdf.ln(10)
                stringCorr = str("Questao " + str(dfResult.loc[i, "CO_POSICAO"])+' '+ DisciplinaCompleto +' ENEM '+str(dfResult.loc[i, "ANO"]) +' '+ str(dfResult.loc[i, "QSEARCH"]))

                link = toYoutube(stringCorr)        
                pdf.add_my_link(170, 25, "RESOLUÇÃO", link)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font('Times', 'B', 12)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print('err')
                continue

    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult['merged'] = dfResult['indexacao'].astype(str) + ' - ' + dfResult['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult), max_cols)]

    # CaCHula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, str('GABARITO '+name), 0, 1, 'C', 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)

    strOut = 'erradas.pdf'            
    pdf.output(strOut, 'F')

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

resultado = resultado[resultado['Acerto'] == 0]

questionNow(resultado)

os.system('cls')
enviar_email('niedsonemanoeltbm@gmail.com')

print(strTri)
print('\n')
print(strResu)
print('\n')

show_results(strResu, strTri)

print('As questões erradas serão enviadas para seu e-mail.')











