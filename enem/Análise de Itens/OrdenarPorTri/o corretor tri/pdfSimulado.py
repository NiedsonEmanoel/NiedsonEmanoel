import pandas as pd
from fpdf import FPDF
from PIL import Image
import os
pd.options.mode.chained_assignment = None
Disciplina = 'CN'

#Definindo Classe do PDF de Saída
class PDF(FPDF):
    def header(self):
        self.image('fundo.png', x=0, y=0, w=self.w, h=self.h, type='png')
        
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'BI', 8)
        # Page number
        self.cell(0, 12, 'Página ' + str(self.page_no()) + '/{nb}' + ' - Simulado por @niedson.studiesmed', 0, 0, 'C')

#Função que gera a lista de Treino de TRI
def geraPDFSIMU(name, dfResult):
    dfResult['indexacao'] = dfResult.reset_index().index + 1
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#LC
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)
    strLC = ''
    for i in dfResult.index:
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.ln(15)
                pdf.ln(15)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('../1. Itens BNI/' + str(dfResult.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('../1. Itens BNI/' + str(dfResult.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'../1. Itens BNI/' + str(dfResult.loc[i, "CO_ITEM"]) + '.png')
                print(strLC)
                continue

    #GAB
    page_width = 190
    cell_width = 63
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult['merged'] = dfResult['indexacao'].astype(str) + ': A[  ]  B[  ]  C[  ]  D[  ]  E[  ]'

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, 'CARTÃO RESPOSTA', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)

    strOut = 'Simulados/' + name + '.pdf'            

    pdf.output(strOut, 'F')


dItens = pd.read_csv('Simulados/simulado'+Disciplina+'.csv', encoding='utf-8', decimal=',')
geraPDFSIMU(Disciplina, dItens)

