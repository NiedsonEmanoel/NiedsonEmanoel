# -*- coding: utf-8 -*-

#dfResult_LC
#linguagens.png
#Linguagens
#LC

import pandas as pd
from fpdf import FPDF
from PIL import Image
import random
import time
import genanki
pd.options.mode.chained_assignment = None
egorger = []

def generate_random_number():
    # Obter o timestamp atual em segundos
    timestamp = int(time.time())

    # Definir o timestamp como semente para a função random
    random.seed(timestamp)

    # Gerar um número inteiro aleatório entre 0 e 100000
    return random.randint(0, 100000)

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

def toYoutube(textPrompt):
    search_query = "https://www.youtube.com/results?search_query=" + "+".join(textPrompt.split())
    return(search_query)


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

#Função que gera a lista de Treino de TRI
def questionBalance_Hab(hab, dfResult):

    dfResult = dfResult.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)
    name = ("H" + str(hab))
    print(name)

    # Para a área de Matemática (LC)
    dfResult_LC = dfResult[dfResult['SG_AREA'] == 'LC']
    dfResult_LC = dfResult_LC[dfResult_LC['CO_HABILIDADE'] == hab]
    dfResult_LC.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_LC['QSEARCH'] = dfResult_LC.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)
    dfResult_LC['indexacao'] = dfResult_LC.reset_index().index + 1

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#LC
    pdf.add_page()
    pdf.image('linguagens.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)

    # Criar um modelo para os flashcards
    modelo = genanki.Model(
        generate_random_number(),
        str(generate_random_number()),
        fields=[
            {'name': 'MyMedia'},
            {'name': 'Questão'},
            {'name': 'Resposta'}
        ],
        templates=[
            {
                'name': 'Cartão 1',
                'qfmt': '<b>{{Questão}}</b><hr>{{MyMedia}}',
                'afmt': '{{FrontSide}}<br><hr><b>{{Resposta}}</b>',
            },
        ])

    # Criar um baralho para armazenar os flashcards
    baralho = genanki.Deck(
        generate_random_number(), # Um número aleatório que identifica o baralho
        str('Habilidades Linguagens:: '+name) # O nome do baralho
    )

    # Criar uma lista para armazenar as informações dos flashcards
    flashcards = []

    # Obter o caminho absoluto da pasta onde estão as imagens
    pasta = os.path.abspath('Itens BNI')

    # Percorrer as linhas do dataframe dfResult_LC
    for i in dfResult_LC.index:
        # Obter o nome do arquivo de imagem da questão
        imagem = str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png'
        caminho_imagem = os.path.join(pasta, imagem)
        
        # Obter a resposta da questão
        resposta = str(dfResult_LC.loc[i, 'TX_GABARITO']) 
        inic = "Q" + str(dfResult_LC.loc[i, "CO_POSICAO"]) + ':' + str(dfResult_LC.loc[i, "ANO"]) + ' - H' + str(dfResult_LC.loc[i, "CO_HABILIDADE"].astype(int)) + " - Proficiência: " + str(dfResult_LC.loc[i, "theta_065"].round(2))

        # Criar um flashcard com a imagem e a resposta
        flashcard = genanki.Note(
            model=modelo,
            fields=[inic,'<img src="https://raw.githubusercontent.com/NiedsonEmanoel/NiedsonEmanoel/main/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI/' + imagem + '"]', resposta]
        )
        
        # Adicionar o flashcard à lista de flashcards
        flashcards.append(flashcard)

    for flashcard in flashcards:
        baralho.add_note(flashcard)

    # Obter o caminho absoluto das imagens
    imagens = [os.path.join(pasta, imagem) for imagem in os.listdir(pasta)]

    # Criar um pacote com o baralho e as imagens
    pacote = genanki.Package(baralho)
    pacote.media_files = imagens
    # Especificar a pasta onde estão as imagens
    pacote.media_folder = pasta

    pacote.write_to_file('Saidas/Flashcards/' + name + '.apkg')

    for i in dfResult_LC.index:
        print("N"+str(dfResult_LC.loc[i, 'indexacao'])+"/"+str(len(dfResult_LC)))
        strLC ="N"+str(dfResult_LC.loc[i, 'indexacao'])+" - Q" + str(dfResult_LC.loc[i, "CO_POSICAO"])+':'+str(dfResult_LC.loc[i, "ANO"]) + ' - H'+str(dfResult_LC.loc[i, "CO_HABILIDADE"].astype(int))+ " - Proficiência: " + str(dfResult_LC.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("CaLCulando...")
        else:
            try:
                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size                
                pdf.set_fill_color(255, 112, 79) 
                pdf.ln(15)
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(10)   # adicionar espaço entre o texto e a imagem



                # caLCular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)
                pdf.ln(10)
                stringCorr = str("Questao " + str(dfResult_LC.loc[i, "CO_POSICAO"])+' Linguagens ENEM '+str(dfResult_LC.loc[i, "ANO"]) +' '+ str(dfResult_LC.loc[i, "QSEARCH"]))

                link = toYoutube(stringCorr)        
                pdf.add_my_link(170, 25, "RESOLUÇÃO", link)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font('Times', 'B', 12)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                erGorger = ("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png - \n'+ strLC +' '+ str(dfResult_LC.loc[i, "CO_PROVA"]))
                egorger.append(erGorger)
                print(erGorger)
                continue

    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_LC['merged'] = dfResult_LC['indexacao'].astype(str) + ' - ' + dfResult_LC['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_LC['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_LC), max_cols)]

    # CaLCula a largura das células de acordo com o número de colunas
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

    strOut = 'Saidas/Habilidades/' + name + '.pdf'            

    pdf.output(strOut, 'F')


dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')
dItens = dItens[dItens['SG_AREA'] == 'LC']

#OTIMIZAÇÃO 
folder_path = os.path.abspath('Itens BNI')
co_items = set(dItens["CO_ITEM"].astype(str))

# Percorra os arquivos na pasta e apague aqueles que não possuem o valor da coluna "CO_ITEM" no seu nome (sem a extensão)
for filename in os.listdir(folder_path):
    name, extension = os.path.splitext(filename)
    if extension == ".png" and name not in co_items:
        os.remove(os.path.join(folder_path, filename))
        print(f"Arquivo excluído: {filename}")
#

for i in range(1, 31):
    if i <= 4 or (i >= 9 and i <= 30):
        questionBalance_Hab(i, dItens)
        print("H" + str(i) + " Pronta!")

print('\nImagens faltando:')
print(egorger)