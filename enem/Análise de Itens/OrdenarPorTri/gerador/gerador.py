import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = './Tesseract/Tesseract.exe'
pd.options.mode.chained_assignment = None

def tri_3pl_enem(theta, a, b, c):
    return c + (1 - c) * (1 / (1 + np.exp(-1.7 * a * (theta - b))))

def imageApi(code):
    code = str(str(code) + '.png')
    imagem = 'https://niedsonemanoel.com.br/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/' + code
    return imagem

def ocrImage(code):
    code = str('../1. Itens BNI/'+str(code) + '.png')
    try:
        img = cv2.imread(code)
        ocrT = str(pytesseract.image_to_string(img, lang='por'))
    except:
        ocrT = 'N/A'
    return ocrT

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

def find_quantile(c):
    return round(((1+c)/2*100), 2)    

def get_prova_string(ano, co_prova):
    if ano == 2016:
        if co_prova in [303]:
            return 'PROVA AZUL'
    if ano == 2017:
        if co_prova in [400, 396]:
            return 'PROVA AMARELA'
        elif co_prova in [406, 393]:
            return 'PROVA CINZA'
        elif co_prova in [436, 440]:
            return 'PROVA AMARELA PPL REAPLICACAO'
        else:
            return 'PROVA CINZA PPL REAPLICACAO'    
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
    if ano == 2022:
        if co_prova in [1056, 1066]:
            return 'PROVA AMARELA'
        elif co_prova in [1078, 1087]:
            return 'PROVA CINZA'
        elif co_prova in [1136, 1146]:
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
   
def thetaToCsv(provas, dfItens):
    dfItens = dfItens[dfItens.CO_PROVA.isin(provas)]
    dfItens["theta_065"] = 0
    countt = 0
    dfItens["imagAPI"] = ''
    dfItens["OCRSearch"] = ''
    dfItens["theta_080"] = 0
    dfItens["theta_099"] = 0
    dfItens["PercentEspAcerto"] = 0
    dfItens['CO_PROVA'] = dfItens.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)

    for i in dfItens.index:    
        dfItens.loc[i, "theta_065"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            0.60,
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
        dfItens.loc[i, 'PercentEspAcerto'] = find_quantile(
            dfItens.loc[i, "NU_PARAM_C"]
        )
        dfItens.loc[i, 'imagAPI'] = imageApi(dfItens.loc[i, 'CO_ITEM'])
        dfItens.loc[i, 'OCRSearch'] = ocrImage(dfItens.loc[i, 'CO_ITEM'])
        print(str(countt)+'/2266')
        countt=countt+1
    return dfItens

def Make():
    #Leitura dos dados de 2016 e Escolha da Prova [303 - MT 2 dia]
#    dItens2014 = pd.read_csv("ITENS_PROVA_2014.csv", sep=";", encoding="latin-1")
    dItens2016 = pd.read_csv("itens_prova_2016.csv", sep=";", encoding="latin-1")
    dItens2017 = pd.read_csv("ITENS_PROVA_2017.csv", sep=";", encoding="latin-1")
    dItens2018 = pd.read_csv("ITENS_PROVA_2018.csv", sep=";", encoding="latin-1")
    dItens2019 = pd.read_csv("ITENS_PROVA_2019.csv", sep=";", encoding="latin-1")
    dItens2020 = pd.read_csv("ITENS_PROVA_2020.csv", sep=";", encoding="latin-1")
    dItens2021 = pd.read_csv("ITENS_PROVA_2021.csv", sep=";", encoding="latin-1")
    dItens2022 = pd.read_csv("ITENS_PROVA_2022.csv", sep=";", encoding="latin-1")

#    provas2014 = [197, 211, 223, 201, 212, 224, 204, 213, 226]
    provas2016 = [303]
    provas2017 = [393,432,396,436,400,440,406,444]
    provas2018 = [449, 488, 452, 492, 456, 496, 462, 500]
    provas2019 = [512, 552, 508, 548, 505, 544, 518, 556]
    provas2020 = [599, 679, 568, 648, 578, 658, 590, 670]
    provas2021 = [911, 991, 880, 960, 890, 970, 902, 982] 
    provas2022 = [1087, 1167, 1056, 1136, 1066, 1146, 1078, 1158] 

    dItens2014['ANO'] = 2014
    dItens2016['ANO'] = 2016
    dItens2017['ANO'] = 2017      
    dItens2018['ANO'] = 2018    
    dItens2019['ANO'] = 2019
    dItens2020['ANO'] = 2020
    dItens2021['ANO'] = 2021
    dItens2022['ANO'] = 2022


    #Colocando as proficiências nas provas e nos dataframes indicados
    dItens2014 = thetaToCsv(provas2014, dItens2014)
    dItens2016 = thetaToCsv(provas2016, dItens2016)
    dItens2017 = thetaToCsv(provas2017, dItens2017)
    dItens2018 = thetaToCsv(provas2018, dItens2018)
    dItens2019 = thetaToCsv(provas2019, dItens2019)
    dItens2020 = thetaToCsv(provas2020, dItens2020)
    dItens2021 = thetaToCsv(provas2021, dItens2021)
    dItens2022 = thetaToCsv(provas2022, dItens2022)
    del dItens2020['TP_VERSAO_DIGITAL']

    result = pd.concat([dItens2014, dItens2016, dItens2017, dItens2018, dItens2019, dItens2020, dItens2021, dItens2022])
    result.to_csv('provasOrdernadasPorTri.csv', index=False, encoding='utf-8', decimal=',')
    result.to_excel("provasOrdernadasPorTri.xlsx")

    return result

Make()



