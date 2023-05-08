import pandas as pd
from fpdf import FPDF
from PIL import Image

pd.options.mode.chained_assignment = None

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
        self.cell(0, 12, 'Página ' + str(self.page_no()) + '/{nb}' + ' por @niedson.studiesmed', 0, 0, 'C')

#Função que gera a lista de Treino de TRI
def questionBalance_65(name, nota_MT, dfResult):

    nota_MTMaior = nota_MT + 200
    nota_MTMenor = nota_MT - 5

    dfResult = dfResult.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    # Para a área de Matemática (MT)
    dfResult_MT = dfResult[dfResult['SG_AREA'] == 'MT']
    dfResult_MT = dfResult_MT[dfResult_MT['theta_065'] <= nota_MTMaior]
    dfResult_MT = dfResult_MT[dfResult_MT['theta_065'] >= nota_MTMenor]
    dfResult_MT.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_MT['indexacao'] = dfResult_MT.reset_index().index + 1


    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#MT
    pdf.add_page()
    pdf.image('matematica.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)

    for i in dfResult_MT.index:
        strLC ="Nº"+str(dfResult_MT.loc[i, 'indexacao'])+" - Q" + str(dfResult_MT.loc[i, "CO_POSICAO"])+':'+str(dfResult_MT.loc[i, "ANO"]) + ' - H'+str(dfResult_MT.loc[i, "CO_HABILIDADE"].astype(int))+ " - Proficiência: " + str(dfResult_MT.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("CaMTulando...")
        else:
            try:
                pdf.set_fill_color(255, 112, 79) 
                pdf.ln(15)
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(10)   # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # caMTular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png')
                print(strLC)
                continue

    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_MT['merged'] = dfResult_MT['indexacao'].astype(str) + ' - ' + dfResult_MT['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_MT['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_MT), max_cols)]

    # CaMTula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, 'GABARITO - Matemática', 0, 1, 'C', 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)

    strOut = 'Saidas/' + name + '_65_TRI.pdf'            

    pdf.output(strOut, 'F')

#Funçao que gera a lista de Revisão da TRI
def questionBalance_99(name, nota_MT, dfResult):

    nota_MTMaior = nota_MT + 200
    nota_MTMenor = nota_MT - 25

    dfResult = dfResult[dfResult['IN_ITEM_ABAN'] == 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 1]

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    dfResult_MT = dfResult[dfResult['SG_AREA'] == 'MT']
    dfResultInterc = dfResult_MT[dfResult_MT['theta_065'] <= nota_MT+200]
    dfResultInterc = dfResult_MT[dfResult_MT['theta_065'] >= nota_MT-5]
    dfResult_MT = dfResult_MT[dfResult_MT['theta_099'] <= nota_MTMaior]
    dfResult_MT = dfResult_MT[dfResult_MT['theta_099'] >= nota_MTMenor]
    dfResult_MT = dfResult_MT[~dfResult_MT['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_MT.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_MT['indexacao'] = dfResult_MT.reset_index().index + 1

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#MT
    pdf.add_page()
    pdf.image('matematica.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)

    for i in dfResult_MT.index:
        strLC ="Q" + str(dfResult_MT.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_MT.loc[i, "ANO"]) + ' - H'+str(dfResult_MT.loc[i, "CO_HABILIDADE"].round(0))+ " - Proficiência: " + str(dfResult_MT.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("CaMTulando...")
        else:
            try:
                pdf.set_fill_color(255, 112, 79) 
                pdf.ln(15)
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(10)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # caMTular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png')
                print(strLC)
                continue
    
    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_MT['merged'] = dfResult_MT['indexacao'].astype(str) + ' - ' + dfResult_MT['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_MT['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_MT), max_cols)]

    # CaMTula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(255, 112, 79)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, 'GABARITO - Matemática', 0, 1, 'C', 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 
    strOut = 'Saidas/' + name + '_99_TRI.pdf'

  
    pdf.output(strOut, 'F') 

#Função que Gera lista de Treino e Revisão TRI
def questionBalance(nome, nota_MT, dfItens):
    questionBalance_65(nome, nota_MT, dfItens)
    questionBalance_99(nome, nota_MT, dfItens)
    print('Concluido!')

dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')

#Gerando as Listas
nome=input("Qual o seu Nome?")
nota_MT = float(input("Qual sua nota TRI em Matemática?"))

questionBalance(nome, nota_MT, dItens)