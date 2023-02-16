import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fpdf import FPDF


def tri_3pl_enem(theta, a, b, c):
    return c + (1 - c) * (1 / (1 + np.exp(-1.7 * a * (theta - b))))


# Plotando a curva do modelo logístico de três parâmetros (TRI)
def plot_graphic(a, b, c):
    theta_vals = np.linspace(-4, 4, num=100)
    y_vals = [tri_3pl_enem(x, a, b, c) for x in theta_vals]

    plt.plot(theta_vals, y_vals)
    plt.xlabel("Valores de theta")
    plt.ylabel("Probabilidade de resposta correta")
    plt.title("Modelo logístico de três parâmetros (TRI)")
    plt.axhline(y=0.65, xmin=-4)
    plt.show()


plot_graphic(2.898, 1.992, 0.097)

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

def get_prova_string(ano, co_prova):
    if ano == 2018:
        if co_prova in [456, 452]:
            return 'PROVA: AMARELA - APLICAÇÃO REGULAR' #CH_LC normal
        elif co_prova in [449, 462]:
            return 'PROVA: CINZA - APLICAÇÃO REGULAR' #CN_MT NORMAL
        elif co_prova in [492, 496]:
            return 'PROVA: AMARELA - APLICAÇÃO PPL' #CH_LC PPL
        else:
            return 'PROVA: CINZA - APLICAÇÃO PPL'  #CN_MT PPL

    if ano == 2019:
        if co_prova in [512, 508]:
            return 'PROVA: AMARELA - APLICAÇÃO REGULAR'
        elif co_prova in [505, 518]:
            return 'PROVA: CINZA - APLICAÇÃO REGULAR'
        elif co_prova in [552, 548]:
            return 'PROVA: AMARELA - APLICAÇÃO PPL'
        else:
            return 'PROVA: CINZA - APLICAÇÃO PPL'

    elif ano == 2020:
        if co_prova in [578, 568]:
            return 'PROVA: AMARELA - APLICAÇÃO REGULAR'
        elif co_prova in [599, 590]:
            return 'PROVA: CINZA - APLICAÇÃO REGULAR'
        elif co_prova in [658, 648]:
            return 'PROVA: AMARELA - APLICAÇÃO PPL'
        else:
            return 'PROVA: CINZA - APLICAÇÃO PPL'
    else:
        if co_prova in [890, 880]:
            return 'PROVA: AMARELA - APLICAÇÃO REGULAR'
        elif co_prova in [902, 911]:
            return 'PROVA: CINZA - APLICAÇÃO REGULAR'
        elif co_prova in [960, 970]:
            return 'PROVA: AMARELA - APLICAÇÃO PPL'
        else:
            return 'PROVA: CINZA - APLICAÇÃO PPL'    

def thetaToCsv(provas, dfItens):
    dfItens = dfItens[dfItens.CO_PROVA.isin(provas)]

    dfItens["theta_065"] = 0
    dfItens["theta_080"] = 0
    dfItens["theta_099"] = 0

    dfItens['CO_PROVA'] = dfItens.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)

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

dItens2018 = pd.read_csv("ITENS_PROVA_2018.csv", sep=";", encoding="latin-1")
provas2018 = [449,488,452,492,456,496,462,500]
dItens2018['ANO'] = 2018    

dItens2019 = pd.read_csv("ITENS_PROVA_2019.csv", sep=";", encoding="latin-1")
provas2019 = [512, 552, 508, 548, 505, 544, 518, 556]
dItens2019['ANO'] = 2019

dItens2020 = pd.read_csv("ITENS_PROVA_2020.csv", sep=";", encoding="latin-1")
provas2020 = [599, 679, 568, 648, 578, 658, 590, 670]
dItens2020['ANO'] = 2020

dItens2021 = pd.read_csv("ITENS_PROVA_2021.csv", sep=";", encoding="latin-1")
provas2021 = [911, 991, 880, 960, 890, 970, 902, 982] 
dItens2021['ANO'] = 2021

dItens2018 = thetaToCsv(provas2018, dItens2018)

dItens2019 = thetaToCsv(provas2019, dItens2019)

dItens2020 = thetaToCsv(provas2020, dItens2020)
del dItens2020['TP_VERSAO_DIGITAL']

dItens2021 = thetaToCsv(provas2021, dItens2021)

result = pd.concat([dItens2018, dItens2019, dItens2020, dItens2021])
result.to_csv('provasOrdernadasPorTri18Ate21.csv', index=False, encoding='utf-8', decimal=',')


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(80)
        StTitle = "Questões para melhora da TRI (2019 - 2021) - "+self.title
        w = self.get_string_width(StTitle) + 6
        self.set_x((210 - w) / 2)
        self.cell(w, 9, StTitle, 0, 0)
        self.ln(20)
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}' + ' por @niedson.studiesmed', 0, 0, 'C')

def questionBalance(name, nota_lc, nota_hm, nota_nat, nota_mat, dfResult):
    nota_lcMaior = nota_lc * 1.07
    nota_lcMenor = nota_lc / 1.07

    nota_hmMaior = nota_hm * 1.07
    nota_hmMenor = nota_hm / 1.07

    nota_natMaior = nota_nat * 1.07
    nota_natMenor = nota_nat / 1.07

    nota_matMaior = nota_mat * 1.07
    nota_matMenor = nota_mat / 1.07

    dfResult = dfResult[dfResult['IN_ITEM_ABAN'] == 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 0]
    dfResult = dfResult[dfResult['TP_LINGUA'] != 1]
    dfResult = dfResult[dfResult['theta_065'] <= 1100]

    cols_to_drop = ['TP_LINGUA', 'TX_MOTIVO_ABAN', 'IN_ITEM_ABAN', 'IN_ITEM_ADAPTADO', 'NU_PARAM_A', 'NU_PARAM_B', 'NU_PARAM_C', 'CO_ITEM']
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
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)
        # Background color
    pdf.set_fill_color(5, 132, 242)
        # Title
    pdf.cell(0, 6, 'LINGUAGENS E CÓDIGOS, QUESTÕES ADAPTADAS A SUA TRI:', 0, 1, 'L', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', '', 12)

    for i in dfResult_LC.index:
        strLC = "Questão " + str(dfResult_LC.loc[i, "CO_POSICAO"]) + " ENEM " + str(dfResult_LC.loc[i, "ANO"]) + " " + str(dfResult_LC.loc[i, "CO_PROVA"]) + "\n- Proficiência: " + str(dfResult_LC.loc[i, "theta_065"].round(2))

        if 'dtype:' in strLC:
            print("ignorar")
        else:
            pdf.set_fill_color(211, 211, 211) 
            pdf.cell(0,10, strLC, 0, 1,'L', 1)   
            pdf.ln(1)
        
#
    pdf.add_page()

    pdf.set_font('Times', 'B', 12)
        # Background color
    pdf.set_fill_color(5, 132, 242)
        # Title
    pdf.cell(0, 6, 'CIÊNCIAS HUMANAS, QUESTÕES ADAPTADAS A SUA TRI:', 0, 1, 'L', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', '', 12)

    for i in dfResult_HM.index:
        strLC = "Questão " + str(dfResult_HM.loc[i, "CO_POSICAO"]) + " ENEM " + str(dfResult_HM.loc[i, "ANO"]) + " " + str(dfResult_HM.loc[i, "CO_PROVA"]) + "\n- Proficiência: " + str(dfResult_HM.loc[i, "theta_065"].round(2))
         
        if 'dtype:' in strLC:
            print("ignorar")
        else:
            pdf.set_fill_color(211, 211, 211) 
            pdf.cell(0,10, strLC, 0, 1,'L', 1)   
            pdf.ln(1)

    pdf.add_page()

    pdf.set_font('Times', 'B', 12)
        # Background color
    pdf.set_fill_color(5, 132, 242)
        # Title
    pdf.cell(0, 6, 'CIÊNCIAS DA NATUREZA, QUESTÕES ADAPTADAS A SUA TRI:', 0, 1, 'L', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', '', 12)

    for i in dfResult_CN.index:
        strLC = "Questão " + str(dfResult_CN.loc[i, "CO_POSICAO"]) + " ENEM " + str(dfResult_CN.loc[i, "ANO"]) + " " + str(dfResult_CN.loc[i, "CO_PROVA"]) + "\n- Proficiência: " + str(dfResult_CN.loc[i, "theta_065"].round(2))
         
        if 'dtype:' in strLC:
            print("ignorar")
        else:
            pdf.set_fill_color(211, 211, 211) 
            pdf.cell(0,10, strLC, 0, 1,'L', 1)   
            pdf.ln(1)

    pdf.add_page()

    pdf.set_font('Times', 'B', 12)
        # Background color
    pdf.set_fill_color(5, 132, 242)
        # Title
    pdf.cell(0, 6, 'MATEMÁTICA, QUESTÕES ADAPTADAS A SUA TRI:', 0, 1, 'L', 1)
        # Line break
    pdf.ln(4)
    pdf.set_font('Times', '', 12)

    for i in dfResult_MT.index:
        strLC = "Questão " + str(dfResult_MT.loc[i, "CO_POSICAO"]) + " ENEM " + str(dfResult_MT.loc[i, "ANO"]) + " " + str(dfResult_MT.loc[i, "CO_PROVA"]) + "\n- Proficiência: " + str(dfResult_MT.loc[i, "theta_065"].round(2))
        if 'dtype:' in strLC:
            print("ignorar")
        else:
            pdf.set_fill_color(211, 211, 211) 
            pdf.cell(0,10, strLC, 0, 1,'L', 1)   
            pdf.ln(1)  

    strOut=name+'_TRI.pdf'            

    pdf.output(strOut, 'F')

questionBalance('Niedson Emanoel Almeida Brito', 625.1, 640.7, 635.5, 684.7, result)

