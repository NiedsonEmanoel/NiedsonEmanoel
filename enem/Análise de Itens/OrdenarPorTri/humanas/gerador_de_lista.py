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
def questionBalance_65(name, nota_hm, dfResult):

    nota_hmMaior = nota_hm + 100
    nota_hmMenor = nota_hm - 5

    dfResult = dfResult.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    # Para a área de Humanas (HM)
    dfResult_HM = dfResult[dfResult['SG_AREA'] == 'CH']
    dfResult_HM = dfResult_HM[dfResult_HM['theta_065'] <= nota_hmMaior]
    dfResult_HM = dfResult_HM[dfResult_HM['theta_065'] >= nota_hmMenor]
    dfResult_HM.sort_values('theta_065', ascending=True, inplace=True)
    dfResult_HM['indexacao'] = dfResult_HM.reset_index().index + 1


    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#HM
    pdf.add_page()
    pdf.image('humanas.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)

    for i in dfResult_HM.index:
        strLC ="Nº"+str(dfResult_HM.loc[i, 'indexacao'])+" - Q" + str(dfResult_HM.loc[i, "CO_POSICAO"])+':'+str(dfResult_HM.loc[i, "ANO"]) + ' - H'+str(dfResult_HM.loc[i, "CO_HABILIDADE"].astype(int))+ " - Proficiência: " + str(dfResult_HM.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(255, 112, 79) 
                pdf.ln(15)
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(10) 
                            # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_HM.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_HM.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_HM.loc[i, "CO_ITEM"]) + '.png')
                print(strLC)
                continue

    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_HM['merged'] = dfResult_HM['indexacao'].astype(str) + ' - ' + dfResult_HM['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_HM['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_HM), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, 'GABARITO - HUMANAS', 0, 1, 'C', 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    strOut = 'Saidas/' + name + '_65_TRI.pdf'            

    pdf.output(strOut, 'F')

#Funçao que gera a lista de Revisão da TRI
def questionBalance_99(name, nota_hm, dfResult):

    nota_hmMaior = nota_hm + 100
    nota_hmMenor = nota_hm - 5

    dfResult = dfResult[dfResult['IN_ITEM_ABAN'] == 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 1]

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    dfResult_HM = dfResult[dfResult['SG_AREA'] == 'CH']
    dfResultInterc = dfResult_HM[dfResult_HM['theta_065'] <= nota_hm+50]
    dfResultInterc = dfResult_HM[dfResult_HM['theta_065'] >= nota_hm-101]
    dfResult_HM = dfResult_HM[dfResult_HM['theta_099'] <= nota_hmMaior]
    dfResult_HM = dfResult_HM[dfResult_HM['theta_099'] >= nota_hmMenor]
    dfResult_HM = dfResult_HM[~dfResult_HM['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_HM.sort_values('theta_065', ascending=True, inplace=True)
    
    dfResult_HM['indexacao'] = dfResult_HM.reset_index().index + 1

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#HM
    pdf.add_page()
    pdf.image('humanas.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)

    for i in dfResult_HM.index:
        strLC ="Nº"+str(dfResult_HM.loc[i, 'indexacao'])+" - Q" + str(dfResult_HM.loc[i, "CO_POSICAO"])+':'+str(dfResult_HM.loc[i, "ANO"]) + ' - H'+str(dfResult_HM.loc[i, "CO_HABILIDADE"].astype(int))+ " - Proficiência: " + str(dfResult_HM.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(89, 162, 165) 
                pdf.ln(15)
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(10)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_HM.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_HM.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_HM.loc[i, "CO_ITEM"]) + '.png')
                print(strLC)
                continue
    
    #GAB
    page_width = 190
    cell_width = 19
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_HM['merged'] = dfResult_HM['indexacao'].astype(str) + ' - ' + dfResult_HM['TX_GABARITO']

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_HM['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_HM), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(255, 112, 79)
    # Title
    pdf.ln(15)
    pdf.cell(0, 10, 'GABARITO - HUMANAS', 0, 1, 'C', 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 
    strOut = 'Saidas/' + name + '_99_TRI.pdf'

    pdf.output(strOut, 'F') 


#Função que Gera lista de Treino e Revisão TRI
def questionBalance(nome, nota_hm, dfItens):
    questionBalance_65(nome, nota_hm, dfItens)
    questionBalance_99(nome, nota_hm, dfItens)
    print('Concluido!')

dItens = pd.read_csv('provasOrdernadasPorTri.csv', encoding='utf-8', decimal=',')

#Gerando as Listas
nome=input("Qual o seu Nome?")
nota_hm = float(input("Qual sua nota TRI em Humanas?"))

questionBalance(nome, nota_hm, dItens)