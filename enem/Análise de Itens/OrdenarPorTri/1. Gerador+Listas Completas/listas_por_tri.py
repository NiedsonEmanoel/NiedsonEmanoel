import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fpdf import FPDF
from PIL import Image

#Função CCI - TRI 3PL
def tri_3pl_enem(theta, a, b, c):
    return c + (1 - c) * (1 / (1 + np.exp(-1.7 * a * (theta - b))))

# Encontrando o valor de theta que resulta em targ (padrão 0.65)
def find_theta(a, b, c, targ):
    left = -100
    right = 100
    tol = 1e-5
    target = targ
    while (right - left) / 2 > tol:
        theta = (left + right) / 2
        value = tri_3pl_enem(theta, a, b, c)
        if value > target:
            right = theta
        else:
            left = theta
    return theta * 100 + 500

#Colocando as proficiências na tabela de itens dos microdados.
def thetaToCsv(provas, dfItens):
    dfItens = dfItens[dfItens.CO_PROVA.isin(provas)]

    dfItens["theta_065"] = 0
    dfItens["theta_080"] = 0
    dfItens["theta_099"] = 0

    for i in dfItens.index:    
        dfItens.loc[i, "theta_065"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.65,
        )
        dfItens.loc[i, "theta_080"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.80,
        )
        dfItens.loc[i, "theta_099"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.99,
        )
    return dfItens


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
def questionBalance_65(name, nota_lc, nota_hm, nota_nat, nota_mat, dfResult):

    nota_lcMaior = nota_lc + 50
    nota_lcMenor = nota_lc - 101

    nota_hmMaior = nota_hm + 50
    nota_hmMenor = nota_hm - 101

    nota_natMaior = nota_nat + 50
    nota_natMenor = nota_nat - 101

    nota_matMaior = nota_mat + 50
    nota_matMenor = nota_mat - 101

    dfResult = dfResult.query("IN_ITEM_ABAN == 0 and TP_LINGUA not in [0, 1]")

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    # Para Linguagens
    dfResult_LC = dfResult[dfResult['SG_AREA'] == 'LC']
    dfResult_LC = dfResult_LC[dfResult_LC['theta_065'] <= nota_lcMaior]
    dfResult_LC = dfResult_LC[dfResult_LC['theta_065'] >= nota_lcMenor]
    dfResult_LC.sort_values('theta_065', ascending=True, inplace=True)

    # Para a área de Humanas (HM)
    dfResult_HM = dfResult[dfResult['SG_AREA'] == 'CH']
    dfResult_HM = dfResult_HM[dfResult_HM['theta_065'] <= nota_hmMaior]
    dfResult_HM = dfResult_HM[dfResult_HM['theta_065'] >= nota_hmMenor]
    dfResult_HM.sort_values('theta_065', ascending=True, inplace=True)

    # Para a área de Ciências da Natureza (CN)
    dfResult_CN = dfResult[dfResult['SG_AREA'] == 'CN']
    dfResult_CN = dfResult_CN[dfResult_CN['theta_065'] <= nota_natMaior]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_065'] >= nota_natMenor]
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)

    # Para a área de Matemática (MT)
    dfResult_MT = dfResult[dfResult['SG_AREA'] == 'MT']
    dfResult_MT = dfResult_MT[dfResult_MT['theta_065'] <= nota_matMaior]
    dfResult_MT = dfResult_MT[dfResult_MT['theta_065'] >= nota_matMenor]
    dfResult_MT.sort_values('theta_065', ascending=True, inplace=True)

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

# MT
    pdf.add_page()
    pdf.image('matematica.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()


    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(89, 162, 165)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE TREINO PARA TRI: MATEMÁTICA', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_MT.index:
        strLC ="Questão " + str(dfResult_MT.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_MT.loc[i, "ANO"]) + ' - H'+str(dfResult_MT.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_MT.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(255, 112, 79) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png')
                continue

    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_MT['merged'] = 'Q'+dfResult_MT['CO_POSICAO'].astype(str) + ' - ' +dfResult_MT['ANO'].astype(str)+ ': ' + dfResult_MT['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_MT['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_MT), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')
    
#LC
    pdf.add_page()
    pdf.image('linguagens.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(89, 162, 165)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE TREINO PARA TRI: LINGUAGENS', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_LC.index:
        strLC ="Questão " + str(dfResult_LC.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_LC.loc[i, "ANO"]) + ' - H'+str(dfResult_LC.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_LC.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
            
                pdf.set_fill_color(255, 112, 79) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png')
                continue

    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_LC['merged'] = 'Q'+dfResult_LC['CO_POSICAO'].astype(str) + ' - ' +dfResult_LC['ANO'].astype(str)+ ': ' + dfResult_LC['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_LC['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_LC), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')

#HM
    pdf.add_page()
    pdf.image('humanas.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(89, 162, 165)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE TREINO PARA TRI: HUMANAS', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_HM.index:
        strLC ="Questão " + str(dfResult_HM.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_HM.loc[i, "ANO"]) + ' - H'+str(dfResult_HM.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_HM.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(255, 112, 79) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

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
                continue

    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_HM['merged'] = 'Q'+dfResult_HM['CO_POSICAO'].astype(str) + ' - ' +dfResult_HM['ANO'].astype(str)+ ': ' + dfResult_HM['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_HM['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_HM), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')

#NT
    pdf.add_page()
    pdf.image('natureza.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()
    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(89, 162, 165)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE TREINO PARA TRI: NATUREZA', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_CN.index:
        strLC ="Questão " + str(dfResult_CN.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_CN.loc[i, "ANO"]) + ' - H'+str(dfResult_CN.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_CN.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(255, 112, 79) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png')
                continue

    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_CN['merged'] = 'Q'+dfResult_CN['CO_POSICAO'].astype(str) + ' - ' +dfResult_CN['ANO'].astype(str)+ ': ' + dfResult_CN['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_CN['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_CN), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(89, 162, 165)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')
    strOut = 'Saidas/' + name + '_65_TRI.pdf'            

    pdf.output(strOut, 'F')

#Funçao que gera a lista de Revisão da TRI
def questionBalance_99(name, nota_lc, nota_hm, nota_nat, nota_mat, dfResult):

    nota_lcMaior = nota_lc + 50
    nota_lcMenor = nota_lc - 101

    nota_hmMaior = nota_hm + 50
    nota_hmMenor = nota_hm - 101

    nota_natMaior = nota_nat + 50
    nota_natMenor = nota_nat - 101

    nota_matMaior = nota_mat + 50
    nota_matMenor = nota_mat - 101

    dfResult = dfResult[dfResult['IN_ITEM_ABAN'] == 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 1]

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C']
    dfResult.drop(cols_to_drop, axis=1, inplace=True)

    # Para a área de Matemática (MT)
    dfResult_MT = dfResult[dfResult['SG_AREA'] == 'MT']
    dfResultInterc = dfResult_MT[dfResult_MT['theta_065'] <= nota_mat+50]
    dfResultInterc = dfResult_MT[dfResult_MT['theta_065'] >= nota_mat-101]
    dfResult_MT = dfResult_MT[dfResult_MT['theta_099'] <= nota_matMaior]
    dfResult_MT = dfResult_MT[dfResult_MT['theta_099'] >= nota_matMenor]
    dfResult_MT = dfResult_MT[~dfResult_MT['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_MT.sort_values('theta_065', ascending=True, inplace=True)

    dfResult_LC = dfResult[dfResult['SG_AREA'] == 'LC']
    dfResultInterc = dfResult_LC[dfResult_LC['theta_065'] <= nota_mat+50]
    dfResultInterc = dfResult_LC[dfResult_LC['theta_065'] >= nota_mat-101]
    dfResult_LC = dfResult_LC[dfResult_LC['theta_099'] <= nota_matMaior]
    dfResult_LC = dfResult_LC[dfResult_LC['theta_099'] >= nota_matMenor]
    dfResult_LC = dfResult_LC[~dfResult_LC['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_LC.sort_values('theta_065', ascending=True, inplace=True)

    dfResult_HM = dfResult[dfResult['SG_AREA'] == 'CH']
    dfResultInterc = dfResult_HM[dfResult_HM['theta_065'] <= nota_mat+50]
    dfResultInterc = dfResult_HM[dfResult_HM['theta_065'] >= nota_mat-101]
    dfResult_HM = dfResult_HM[dfResult_HM['theta_099'] <= nota_matMaior]
    dfResult_HM = dfResult_HM[dfResult_HM['theta_099'] >= nota_matMenor]
    dfResult_HM = dfResult_HM[~dfResult_HM['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_HM.sort_values('theta_065', ascending=True, inplace=True)

    dfResult_CN = dfResult[dfResult['SG_AREA'] == 'CN']
    dfResultInterc = dfResult_CN[dfResult_CN['theta_065'] <= nota_mat+50]
    dfResultInterc = dfResult_CN[dfResult_CN['theta_065'] >= nota_mat-101]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_099'] <= nota_matMaior]
    dfResult_CN = dfResult_CN[dfResult_CN['theta_099'] >= nota_matMenor]
    dfResult_CN = dfResult_CN[~dfResult_CN['theta_065'].isin(dfResultInterc['theta_065'])]
    dfResult_CN.sort_values('theta_065', ascending=True, inplace=True)



    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_title(name)

#MT
    pdf.add_page()
    pdf.image('matematica.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(255, 112, 79)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE REVISÃO PARA TRI: MATEMÁTICA', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_MT.index:
        strLC ="Questão " + str(dfResult_MT.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_MT.loc[i, "ANO"]) + ' - H'+str(dfResult_MT.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_MT.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(89, 162, 165) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_MT.loc[i, "CO_ITEM"]) + '.png')
                continue
    
    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_MT['merged'] = 'Q'+dfResult_MT['CO_POSICAO'].astype(str) + ' - ' +dfResult_MT['ANO'].astype(str)+ ': ' + dfResult_MT['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_MT['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_MT), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(255, 112, 79)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 
    strOut = 'Saidas/' + name + '_99_TRI.pdf'

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')

#LC
    pdf.add_page()
    pdf.image('linguagens.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(255, 112, 79)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE REVISÃO PARA TRI: LINGUAGENS', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_LC.index:
        strLC ="Questão " + str(dfResult_LC.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_LC.loc[i, "ANO"]) + ' - H'+str(dfResult_LC.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_LC.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(89, 162, 165) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_LC.loc[i, "CO_ITEM"]) + '.png')
                continue
    
    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_LC['merged'] = 'Q'+dfResult_LC['CO_POSICAO'].astype(str) + ' - ' +dfResult_LC['ANO'].astype(str)+ ': ' + dfResult_LC['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_LC['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_LC), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(255, 112, 79)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 
    strOut = 'Saidas/' + name + '_99_TRI.pdf'

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')

#CH
    pdf.add_page()
    pdf.image('humanas.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(255, 112, 79)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE REVISÃO PARA TRI: HUMANAS', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_HM.index:
        strLC ="Questão " + str(dfResult_HM.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_HM.loc[i, "ANO"]) + ' - H'+str(dfResult_HM.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_HM.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(89, 162, 165) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

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
                continue
    
    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_HM['merged'] = 'Q'+dfResult_HM['CO_POSICAO'].astype(str) + ' - ' +dfResult_HM['ANO'].astype(str)+ ': ' + dfResult_HM['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_HM['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_HM), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(255, 112, 79)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 
    strOut = 'Saidas/' + name + '_99_TRI.pdf'

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')

#CN
    pdf.add_page()
    pdf.image('natureza.png', x=0, y=0, w=pdf.w, h=pdf.h, type='png')
    pdf.add_page()

    pdf.set_font('Times', 'B', 14)
        # Background color
    pdf.set_fill_color(255, 112, 79)
        # Title
    pdf.cell(0, 6, 'QUESTÕES DE REVISÃO PARA TRI: NATUREZA', 0, 1, 'C', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', 'B', 12)

    for i in dfResult_CN.index:
        strLC ="Questão " + str(dfResult_CN.loc[i, "CO_POSICAO"])+" - ENEM " + str(dfResult_CN.loc[i, "ANO"]) + ' - H'+str(dfResult_CN.loc[i, "CO_HABILIDADE"])+ " - Proficiência: " + str(dfResult_CN.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("Calculando...")
        else:
            try:
                pdf.set_fill_color(89, 162, 165) 
                pdf.cell(0, 10, strLC, 0, 1, 'C', 1)
                pdf.ln(5)  # adicionar espaço entre o texto e a imagem

                # obter as dimensões da imagem
                with Image.open('Itens BNI/' + str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png') as img:
                    img.thumbnail((160, 160))

                    # obter as dimensões da imagem redimensionada
                    width, height = img.size

                # calcular a posição y para centralizar a imagem
                y = pdf.get_y()

                # ajustar as coordenadas de posição e o tamanho da imagem
                pdf.image('Itens BNI/' + str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png', x=pdf.w / 2 - width / 2, y=y, w=width, h=height)

                # adicionar quebra de página
                pdf.add_page()
            except FileNotFoundError:
                print("Arquivo de imagem não encontrado: "+'Itens BNI/' + str(dfResult_CN.loc[i, "CO_ITEM"]) + '.png')
                continue
    
    #GAB
    page_width = 190
    cell_width = 38
    max_cols = int(page_width / cell_width)

    # Junta as colunas do dataframe
    dfResult_CN['merged'] = 'Q'+dfResult_CN['CO_POSICAO'].astype(str) + ' - ' +dfResult_CN['ANO'].astype(str)+ ': ' + dfResult_CN['TX_GABARITO'].astype(str)

    # Divide os dados em grupos de até max_cols colunas
    data = [dfResult_CN['merged'][i:i+max_cols].tolist() for i in range(0, len(dfResult_CN), max_cols)]

    # Calcula a largura das células de acordo com o número de colunas
    cell_width = page_width / max_cols

    # Cria a tabela
    pdf.set_fill_color(255, 112, 79)
    # Title
    pdf.cell(0, 6, 'GABARITO', 0, 1, 'C', 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)

    for row in data:
        for col in row:
            pdf.cell(cell_width, 10, col, 1, 0, 'C')
        pdf.ln() # quebra de linha para a próxima linha da tabela 
    strOut = 'Saidas/' + name + '_99_TRI.pdf'

    pdf.ln(5)
    pdf.set_font('Arial', 'BI', 8)
    pdf.cell(0, 10, '*Mesma ordem da lista', 0, 0, 'L')     

    pdf.output(strOut, 'F')  

#Função que Gera lista de Treino e Revisão TRI
def questionBalance(nome, nota_lc, nota_hm, nota_nat, nota_mat, dfItens):
    questionBalance_65(nome, nota_lc, nota_hm, nota_nat, nota_mat, dfItens)
    questionBalance_99(nome, nota_lc, nota_hm, nota_nat, nota_mat, dfItens)
    print('Concluido!')

#Leitura dos dados de 2016 e Escolha da Prova [303 - MT 2 dia]
dItens2016 = pd.read_csv("itens_prova_2016.csv", sep=";", encoding="latin-1")
dItens2018 = pd.read_csv("ITENS_PROVA_2018.csv", sep=";", encoding="latin-1")
dItens2019 = pd.read_csv("ITENS_PROVA_2019.csv", sep=";", encoding="latin-1")
dItens2020 = pd.read_csv("ITENS_PROVA_2020.csv", sep=";", encoding="latin-1")
dItens2021 = pd.read_csv("ITENS_PROVA_2021.csv", sep=";", encoding="latin-1")

provas2016 = [303]
provas2018 = [449,488,452,492,456,496,462,500]
provas2019 = [512, 552, 508, 548, 505, 544, 518, 556]
provas2020 = [599, 679, 568, 648, 578, 658, 590, 670]
provas2021 = [911, 991, 880, 960, 890, 970, 902, 982] 

dItens2016['ANO'] = 2016    
dItens2018['ANO'] = 2018    
dItens2019['ANO'] = 2019
dItens2020['ANO'] = 2020
dItens2021['ANO'] = 2021


#Colocando as proficiências nas provas e nos dataframes indicados
dItens2016 = thetaToCsv(provas2016, dItens2016)
dItens2018 = thetaToCsv(provas2018, dItens2018)
dItens2019 = thetaToCsv(provas2019, dItens2019)
dItens2020 = thetaToCsv(provas2020, dItens2020)
dItens2021 = thetaToCsv(provas2021, dItens2021)
del dItens2020['TP_VERSAO_DIGITAL']

result = pd.concat([dItens2016,dItens2018, dItens2019, dItens2020, dItens2021])
result.to_csv('provasOrdernadasPorTri.csv', index=False, encoding='utf-8', decimal=',')

#Gerando as Listas
nome=input("Qual o seu Nome?")
nota_lc = float(input("Qual sua nota TRI em Linguagens?"))
nota_hm = float(input("Qual sua nota TRI em Humanas?"))
nota_nat = float(input("Qual sua nota TRI em Natureza?"))
nota_mat = float(input("Qual sua nota TRI em Matemática?"))

questionBalance(nome, nota_lc, nota_hm, nota_nat, nota_mat, result)