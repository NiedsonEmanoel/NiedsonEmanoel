import pandas as pd
import numpy as np
import time
import random
import plotly.express as px
import numpy as np
import genanki
from fpdf import FPDF
import requests
from io import BytesIO
from PIL import Image
import string
import os
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import barcode
import zipfile
from barcode.writer import ImageWriter
from concurrent.futures import ThreadPoolExecutor


def flashnamesa(SG):
    if SG == 'CN': return 'Natureza'
    elif SG == 'MT': return 'Matemática'
    elif SG == 'CH': return 'Humanas'
    else: return 'Linguagens'

#Definindo Classe do PDF de Saída
class PDF(FPDF):
    def header(self):
       self.image('images/fundo.png', x=0, y=0, w=self.w, h=self.h, type='png')

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
      if self.page_no() != 1:
        self.image("images/fundo2.png", x=90, y=283, h=10,type='png')
        self.set_y(0)
        self.set_font('Arial', 'BI', 8)
        self.cell(0, 8, '     '+str(self.page_no()) + '/{nb}', 0, 0, 'C')

def toYoutube(textPrompt):
    try:
      search_query = "https://www.youtube.com/results?search_query=" + "+".join(textPrompt.split())
    except:
      search_query = 'N/A'
    return(search_query)

def remover_caracteres_invalidos(texto):
        numAssc = 251
        try:
          caracteres_invalidos = [char for char in texto if ord(char) > numAssc]
          texto_substituido = ''.join('' if ord(char) > numAssc else char for char in texto)
          print(f"Caracteres inválidos substituídos: {caracteres_invalidos}")
          return texto_substituido
        except:
          print('sorry')
          return(texto)

def generate_random_number():
    # Gerar um número inteiro aleatório entre 0 e 100000
    return random.randint(0, 100000)


def questHab(dfResult_CN, name):
    try:
        cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
        dfResult.drop(cols_to_drop, axis=1, inplace=True)
    except:
        pass

    flashnames = name
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_CN['indexacao'] = dfResult_CN.reset_index().index + 1

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(flashnames)

    pdf.add_page()
    pdf.image("images/wordcloud_a4.png", x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)
    img_dir = 'images/'  # Diretório local para salvar as imagens

    # Criar diretório se não existir
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)


    for i in dfResult_CN.index:
        print("N"+str(dfResult_CN.loc[i, 'indexacao'])+"/"+str(len(dfResult_CN)))
        strCN ="N"+str(dfResult_CN.loc[i, 'indexacao'])+" - Q" + str(dfResult_CN.loc[i, "CO_POSICAO"])+':'+str(dfResult_CN.loc[i, "ANO"]) + ' - H'+str(dfResult_CN.loc[i, "CO_HABILIDADE"].astype(int))+ " - Proficiência: " + str(dfResult_CN.loc[i, "theta_065"].round(2))
        if 'dtype:' in strCN:
            print("...")
        else:
            try:
                pdf.ln(15)  # adicionar espaço entre o texto e a imagem
                img_filename = f"{dfResult_CN.loc[i, 'CO_ITEM']}.png"
                img_path = os.path.join(img_dir, img_filename)

                codestr = f"{dfResult_CN.loc[i, 'CO_ITEM']}"

                img_pathax = os.path.join(img_dir, str('xa'+codestr))

                code128 = barcode.get("code128", codestr, writer=ImageWriter())
                filename = code128.save(img_pathax)
                img_pathax = img_pathax+'.png'

                # Verificar se a imagem já foi baixada
                if not os.path.exists(img_path):
                    url = 'https://niedsonemanoel.com.br/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/'+ str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png'
                    response = requests.get(url)

                    with open(img_path, 'wb') as img_file:
                        img_file.write(response.content)
                        print(img_path)

                # Abrir a imagem do diretório local
                with Image.open(img_path) as img:
                    img.thumbnail((160, 160))
                    width, height = img.size

                pdf.set_fill_color(255, 112, 79)
             #   pdf.ln(15)
                pdf.cell(0, 10, strCN, 0, 1, 'C', 1)
                pdf.ln(10)   # adicionar espaço entre o texto e a imagem

                # caCNular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image(img_path, x=pdf.w / 2 - width / 2, y=y, w=width, h=height)
                pdf.image(img_pathax, x=3, y=-3,  h=25) #w=45,
                pdf.ln(10)

                link = toYoutube(remover_caracteres_invalidos(dfResult_CN.loc[i, "OCRSearch"]))
                pdf.add_my_link(170, 25, "RESOLUÇÃO", link)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font('Times', 'B', 12)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print(strCN)
                continue

    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_CN['merged'] = dfResult_CN['indexacao'].astype(str) + ' - ' + dfResult_CN['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_CN['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_CN), max_cols)]

    # CaCNula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, str('GABARITO'), 0, 1, 'C', 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)

    strOut =str('Saida_Itens_Processados/'+name)+ '.pdf'

    pdf.output(strOut, 'F')
    dfResult_CN.to_excel(str('Saida_Itens_Processados/'+name)+ '.xlsx')

    return strOut


df = pd.read_csv('../provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
df = df.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

naoTemCorrecaoComentada = []
temCorrecaoComentada = []

for i in df.index:
    caminho_do_arquivo = '../../1. Itens BNI_/Correcao/'+str(df.loc[i, "CO_ITEM"])+'.gif'
    if os.path.exists(caminho_do_arquivo):
        temCorrecaoComentada.append(df.loc[i])
    else:
        naoTemCorrecaoComentada.append(df.loc[i])

temCorrecaoComentada = pd.DataFrame(temCorrecaoComentada)
naoTemCorrecaoComentada = pd.DataFrame(naoTemCorrecaoComentada)

naoTemCorrecaoComentada_CH = naoTemCorrecaoComentada[naoTemCorrecaoComentada['SG_AREA'] == 'CH']
naoTemCorrecaoComentada_LC = naoTemCorrecaoComentada[naoTemCorrecaoComentada['SG_AREA'] == 'LC']
naoTemCorrecaoComentada_CN = naoTemCorrecaoComentada[naoTemCorrecaoComentada['SG_AREA'] == 'CN']
naoTemCorrecaoComentada_MT = naoTemCorrecaoComentada[naoTemCorrecaoComentada['SG_AREA'] == 'MT']


def process_area(df_area, output_filename):
    questHab(df_area, output_filename)

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    executor.submit(process_area, naoTemCorrecaoComentada_CH, 'Sem_Correcao_Humanas')
    executor.submit(process_area, naoTemCorrecaoComentada_LC, 'Sem_Correcao_Linguagens')
    executor.submit(process_area, naoTemCorrecaoComentada_CN, 'Sem_Correcao_Natureza')
    executor.submit(process_area, naoTemCorrecaoComentada_MT, 'Sem_Correcao_Matemática')