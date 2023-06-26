Disciplina = input("Digite a sigla da disciplina desejada: MT, LC, CH, CN: ").upper()
Email = input('Digite seu email: ')
qtdtt =(int(input('Digite a quantidade de Questões [12 - 45]: ')))

if (qtdtt>=45):
    qtdtt = 45
elif(qtdtt<=12):
    qtdtt = 12
else:
    qtdtt = qtdtt

qtdQuestoes = qtdtt
pComple = 0

if (qtdQuestoes == 45):
    provaComple = (input('Prova completa? [S ou N | Y or N]: ')).upper()
    if((provaComple == 'S') or (provaComple == 'Y')):
        pComple = 1
    else:
        pComple = 0
        
proficiencia_inicial = 0

if(pComple == 0):
    proficiencia_inicial = ((float(input("Digite a proficiência inicial: "))+500)/2)

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
timeExec = 0
dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
dItens = dItens[dItens['SG_AREA'] == Disciplina]
dItens = dItens.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

if (qtdtt>=45):
    qtdtt = 45
elif(qtdtt<=12):
    qtdtt = 12
else:
    qtdtt = qtdtt

qtdQuestoes = qtdtt

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
        self.image('fundo.png', x=0, y=0, w=self.w, h=self.h, type='png')

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

def converter_tempo(s):
    segundos = int(s)
    minutos = segundos // 60
    segundos %= 60
    horas = minutos // 60
    minutos %= 60

    tempo_formatado = "{:02d}h {:02d}min {:02d}s".format(horas, minutos, segundos)
    return tempo_formatado

def show_image(image_path, zoom, quaestNow, timeExec):
    pygame.init()
    l = timeExec
    font = pygame.font.Font(None, 40)
    fontTime = pygame.font.Font(None, 40)

    text_color = (0, 0, 0)

    tst = str(quaestNow)+ '/' +str(qtdQuestoes)
    tstRendered = font.render(tst, True, text_color)

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

    left_click_color = (0, 0, 0)  # Caneta preta
    draw_color = None  # Cor de desenho atual

    all_drawings = []  # Lista para armazenar todas as marcações
    current_drawing = []  # Lista para armazenar os pontos da marcação atual
    marker_size = 5  # Tamanho inicial do marcador
    drawing = False  # Flag para indicar se o mouse está sendo pressionado para desenhar

    running = True
    while running:
        l = l+1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    resposta = 'A'
                    running = False
                elif event.key == pygame.K_UP:  # Seta para cima
                    image_rect.y -= 10
                elif event.key == pygame.K_DOWN:  # Seta para baixo
                    image_rect.y += 10
                elif event.key == pygame.K_RIGHT:  # Seta para direita
                    image_rect.x += 10
                elif event.key == pygame.K_LEFT:  # Seta para esquerda
                    image_rect.x -= 10
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
                elif event.key == pygame.K_0:
                    scaled_image = original_image.resize((int(image_width ), int(image_height)))
                    image = pygame.image.fromstring(scaled_image.tobytes(), scaled_image.size, scaled_image.mode)
                    image_rect = image.get_rect(center=screen.get_rect().center)
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
                elif event.key == pygame.K_KP_MULTIPLY or event.key == pygame.K_ASTERISK:
                    marker_size += 1
                elif event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                    marker_size -= 1
                    if marker_size < 1:
                        marker_size = 1
                elif event.key == pygame.K_l:
                    all_drawings = []

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    draw_color = left_click_color

                drawing = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    all_drawings.append(current_drawing)
                    current_drawing = []
                    drawing = False

        if drawing:
            # Adiciona o ponto atual do mouse à marcação atual
            current_drawing.append(pygame.mouse.get_pos())

        s = l/60
        tempo_formatado = converter_tempo(s)

        timeRendered = fontTime.render(str(tempo_formatado), True, text_color)

        screen.fill((255, 255, 255))
        screen.blit(tstRendered, (screen_width/2.05, 50))
        screen.blit(timeRendered, (screen_width/2.2, screen_height-30))
        screen.blit(image, image_rect)

        # Desenha todas as marcações
        for drawing_points in all_drawings:
            if len(drawing_points) > 1:
                pygame.draw.lines(screen, draw_color, False, drawing_points, marker_size)

        # Desenha a marcação atual separadamente
        if len(current_drawing) > 1:
            pygame.draw.lines(screen, draw_color, False, current_drawing, marker_size)

        pygame.display.flip()
        clock.tick(60)

    return resposta, l

def show_results(results, triString, timeExec):
    pygame.init()
    timeExec = timeExec/60
    timeExec = converter_tempo(timeExec)
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
        
        TotalTime = 'Tempo total: '+timeExec

        rende = font.render(TotalTime, True, text_color)
        screen.blit(rende, (screen_width/2.65, 150))

        pygame.display.flip()
        clock.tick(60)

def jogo_proficiencia(df, timeExec):
    quaestNow = 1
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

        resposta, l = show_image(caminho_imagem, 1.0, quaestNow, timeExec)
        timeExec=+l
        resposta = resposta.upper()
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

        quaestNow = quaestNow+1
    return pd_resultado, timeExec

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
    smtp_password='hpvepsdpvtstsjiz'

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

def createSampre(dItens):
    dItens = dItens[dItens['CO_HABILIDADE'].between(1, 30)]
    dItens = dItens[dItens['IN_ITEM_ABAN'] == 0]

    dItens.sort_values('theta_065', ascending=True, inplace=True)

    if Disciplina == 'LC':
        dItens = dItens[~dItens['CO_HABILIDADE'].isin([5, 6, 7, 8])]

    # Selecionar um item de cada habilidade de 1 a 30
    habilidades_unicas = dItens.groupby('CO_HABILIDADE').sample(1)

    # Selecionar os 12 itens restantes permitindo repetições, mas no máximo 3 repetições por habilidade
    habilidades_repetidas = dItens.groupby('CO_HABILIDADE').apply(lambda x: x.sample(min(len(x), 3)))
    habilidades_repetidas = habilidades_repetidas.sample(n=12, replace=True)

    # Combinar os dataframes resultantes
    resultado = pd.concat([habilidades_unicas, habilidades_repetidas])

    # Obter as habilidades presentes no resultado atual
    habilidades_presentes = resultado['CO_HABILIDADE'].unique()

    # Verificar se todas as 30 habilidades estão presentes
    if Disciplina != 'LC':
        if len(habilidades_presentes) < 30:
            # Calcular o número de habilidades faltantes
            habilidades_faltantes = np.setdiff1d(range(1, 31), habilidades_presentes)
            num_faltantes = 30 - len(habilidades_presentes)

            # Selecionar itens adicionais para as habilidades faltantes
            itens_faltantes = dItens[dItens['CO_HABILIDADE'].isin(habilidades_faltantes)].sample(n=num_faltantes, replace=True)

            # Combinar os itens faltantes com os resultados atuais
            resultado = pd.concat([resultado, itens_faltantes])

    # Verificar o número de itens atual
    num_itens = len(resultado)

    # Remover itens extras se o número atual for maior que 45
    if num_itens > 45:
        resultado = resultado.sample(n=45)

    # Preencher com itens adicionais se o número atual for menor que 45
    if num_itens < 45:
        num_adicionais = 45 - num_itens
        itens_adicionais = dItens.sample(n=num_adicionais, replace=True)
        resultado = pd.concat([resultado, itens_adicionais])
    
    resultado = resultado.sample(frac=1)

    return resultado

def jogoQuarentaECinco(df, timeExec):
    quaestNow = 1
    pd_resultado = pd.DataFrame(columns=['TX_GABARITO', 'ANO', 'CO_PROVA', "CO_POSICAO", 'CO_HABILIDADE','NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'CO_ITEM', 'theta_065', 'Acerto'])

    items_visitados = set()  # Conjunto para armazenar os itens já visitados

    while quaestNow <= qtdQuestoes:
        itens_disponiveis = df.loc[~df['CO_ITEM'].isin(items_visitados)]
        if len(itens_disponiveis) == 0:
            break  # Todos os itens já foram visitados, interrompe o loop

        questao = itens_disponiveis.sample(n=1).iloc[0]

        caminho_imagem = '../1. Itens BNI/' + str(questao['CO_ITEM']) + '.png'
        gabarito = questao['TX_GABARITO']

        resposta, l = show_image(caminho_imagem, 1.0, quaestNow, timeExec)
        timeExec = l
        
        resposta = resposta.upper()
        if resposta == gabarito:
            acerto = 1
        else:
            acerto = 0

        pd_resultado = pd_resultado.append({
            'CO_PROVA': questao['CO_PROVA'],
            'CO_POSICAO': questao['CO_POSICAO'],
            'TX_GABARITO': questao['TX_GABARITO'],
            'CO_ITEM': questao['CO_ITEM'],
            'ANO': questao['ANO'],
            'CO_HABILIDADE': questao['CO_HABILIDADE'],
            'NU_PARAM_A': questao['NU_PARAM_A'],
            'NU_PARAM_B': questao['NU_PARAM_B'],
            'NU_PARAM_C': questao['NU_PARAM_C'],
            'theta_065': questao['theta_065'],
            'Acerto': acerto
        }, ignore_index=True)

        items_visitados.add(questao['CO_ITEM'])  # Adiciona o item visitado ao conjunto

        quaestNow += 1
    return pd_resultado, timeExec

if (pComple == 1):
    dItens = createSampre(dItens)
    resultado, timeExecsA = jogoQuarentaECinco(dItens, timeExec)

if(pComple == 0):
    resultado, timeExecsS = jogo_proficiencia(dItens, timeExec)

a, b, c, x = zip(*resultado[['NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'Acerto']].values.tolist())

if (pComple == 1):
    timeExec = timeExecsA

if(pComple == 0):
    timeExec = timeExecsS


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
print('As questões erradas serão enviadas para seu e-mail. '+Email)
print('')
enviar_email(Email)

print(strTri)
print('\n')
print(strResu)
print('\n')

show_results(strResu, strTri, timeExec)

