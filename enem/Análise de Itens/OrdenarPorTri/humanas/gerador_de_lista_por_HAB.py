# -*- coding: utf-8 -*-

#dfResult_CH
#humanas.png
#Humanas
#CH

import pandas as pd
from fpdf import FPDF
from PIL import Image

pd.options.mode.chained_assignment = None

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

    # Para a área de Matemática (CH)
    dfResult_CH = dfResult[dfResult['SG_AREA'] == 'CH']
    dfResult_CH = dfResult_CH[dfResult_CH['CO_HABILIDADE'] == hab]
    dfResult_CH.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_CH['QSEARCH'] = dfResult_CH.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)
    dfResult_CH['indexacao'] = dfResult_CH.reset_index().index + 1

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#CH
    pdf.add_page()
    pdf.image('humanas.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)

    for i in dfResult_CH.index:
        print("N"+str(dfResult_CH.loc[i, 'indexacao'])+"/"+str(len(dfResult_CH)))
        strCH ="N"+str(dfResult_CH.loc[i, 'indexacao'])+" - Q" + str(dfResult_CH.loc[i, "CO_POSICAO"])+':'+str(dfResult_CH.loc[i, "ANO"]) + ' - H'+str(dfResult_CH.loc[i, "CO_HABILIDADE"].astype(int))+ " - Proficiência: " + str(dfResult_CH.loc[i, "theta_065"].round(2))
        if 'dtype:' in strCH:
            print("CaCHulando...")
        else:
            try:
                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_CH.loc[i, "CO_ITEM"]) + '.png') as img:
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
                pdf.image('Itens BNI/' + str(dfResult_CH.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)
                pdf.ln(10)
                stringCorr = str("Questao " + str(dfResult_CH.loc[i, "CO_POSICAO"])+' Humanas ENEM '+str(dfResult_CH.loc[i, "ANO"]) +' '+ str(dfResult_CH.loc[i, "QSEARCH"]))

                link = toYoutube(stringCorr)        
                pdf.add_my_link(170, 25, "RESOLUÇÃO", link)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font('Times', 'B', 12)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_CH.loc[i, "CO_ITEM"]) + '.png')
                print(strCH)
                continue

    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_CH['merged'] = dfResult_CH['indexacao'].astype(str) + ' - ' + dfResult_CH['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_CH['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_CH), max_cols)]

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

    strOut = 'Saidas/Habilidades/' + name + '.pdf'            

    pdf.output(strOut, 'F')


dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')

for i in range(1, 31):
    questionBalance_Hab(i, dItens)
    print("H" + str(i) + " Pronta!")




    
