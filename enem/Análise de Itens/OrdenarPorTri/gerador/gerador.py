import cv2
import numpy as np
import requests
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = './Tesseract/Tesseract.exe'
pd.options.mode.chained_assignment = None

def tri_3pl_enem(theta, a, b, c):
    return c + (1 - c) / (1 + np.exp(-a * (theta - b)))
    
def imageApi(code):
    code = str(str(code) + '.png')
    imagem = 'https://niedsonemanoel.com.br/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/' + code
    return imagem

def ocrImage(code):
    output_file='../1. Itens BNI_/TXT/'+str(code)+'.txt'
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as file:
            return file.read()

    code = 'https://raw.githubusercontent.com/NiedsonEmanoel/NiedsonEmanoel/main/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/1.%20Itens%20BNI_/'+str(str(code) + '.png')
    try:
        response = requests.get(code)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)

        # Decodificar a imagem usando o OpenCV
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        ocrT = str(pytesseract.image_to_string(img, lang='por'))

        # Salvar o resultado no arquivo .txt se o arquivo não existir
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(ocrT)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
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
    if ano == 2014:
      if co_prova in [197, 201]:
          return 'PROVA BRANCA REGULAR'
      elif co_prova in [211, 212]:
          return 'PROVA BRANCA PPL1'
      elif co_prova in [223, 224]:
          return 'PROVA BRANCA PPL2'
      elif co_prova in [204, 208]:
          return 'PROVA CINZA REGULAR'
      elif co_prova in [213, 214]:
          return 'PROVA CINZA PPL1'
      else:
          return 'PROVA CINZA PPL2'
    if ano == 2015:
        if co_prova in [232, 236]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [240, 244]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [272, 276]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
    if ano == 2016:
        if co_prova in [303]:
            return 'PROVA AZUL REGULAR'
        if co_prova in [296, 292]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [302]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [337, 332]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
    if ano == 2017:
        if co_prova in [400, 396]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [406, 393]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [436, 440]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
    if ano == 2018:
        if co_prova in [456, 452]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [449, 462]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [496, 492]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
    if ano == 2019:
        if co_prova in [512, 508]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [505, 518]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [552, 548]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
    if ano == 2020:

        if co_prova in [578, 568]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [599, 590]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [658, 648]:
            return 'PROVA AMARELA PPL'
        elif co_prova == 688:
            return 'HUMANAS DIGITAL AMARELA'
        elif co_prova == 692:
            return 'LINGUAGENS DIGITAL AMARELA'
        elif co_prova == 700:
            return 'NATUREZA DIGITAL AMARELA'
        elif co_prova == 696:
            return 'MATEMATICA DIGITAL AMARELA'
        else:
            return 'PROVA CINZA PPL'
    if ano == 2022:
        if co_prova in [1056, 1066]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [1078, 1087]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [1136, 1146]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
    else: #2021
        if co_prova in [890, 880]:
            return 'PROVA AMARELA REGULAR'
        elif co_prova in [902, 911]:
            return 'PROVA CINZA REGULAR'
        elif co_prova in [960, 970]:
            return 'PROVA AMARELA PPL'
        else:
            return 'PROVA CINZA PPL'
   
def thetaToCsv(provas, dfItens):
    dfItens = dfItens[dfItens.CO_PROVA.isin(provas)]
    dfItens["theta_065"] = 0
    countt = 1
    numero_de_linhas = len(dfItens)
    dfItens["imagAPI"] = ''
    dfItens["OCRSearch"] = ''
    dfItens["theta_080"] = 0
    dfItens["theta_099"] = 0
    dfItens["PercentEspAcerto"] = 0
    dfItens['IN_ENCCEJA'] = 0
    dfItens['IN_ENEM'] = 1
    dfItens['CO_PROVA'] = dfItens.apply(lambda row: get_prova_string(row['ANO'], row['CO_PROVA']), axis=1)

    for i in dfItens.index:    
        dfItens.loc[i, "theta_065"] = find_theta(
            dfItens.loc[i, "NU_PARAM_A"],
            dfItens.loc[i, "NU_PARAM_B"],
            dfItens.loc[i, "NU_PARAM_C"],
            (find_quantile(dfItens.loc[i, "NU_PARAM_C"])/100),
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
        print(str(countt)+'/'+str(numero_de_linhas)+' - '+str(dfItens.loc[i, 'ANO']))
        countt=countt+1
    return dfItens

def Make():

    dItens2014 = pd.read_csv("ITENS_PROVA_2014.csv", sep=";", encoding="latin-1")
    dItens2015 = pd.read_csv("ITENS_PROVA_2015.csv", sep=";", encoding="latin-1")
    dItens2016 = pd.read_csv("itens_prova_2016.csv", sep=";", encoding="latin-1")
    dItens2017 = pd.read_csv("ITENS_PROVA_2017.csv", sep=";", encoding="latin-1")
    dItens2018 = pd.read_csv("ITENS_PROVA_2018.csv", sep=";", encoding="latin-1")
    dItens2019 = pd.read_csv("ITENS_PROVA_2019.csv", sep=";", encoding="latin-1")
    dItens2020 = pd.read_csv("ITENS_PROVA_2020.csv", sep=";", encoding="latin-1")
    dItens2021 = pd.read_csv("ITENS_PROVA_2021.csv", sep=";", encoding="latin-1")
    dItens2022 = pd.read_csv("ITENS_PROVA_2022.csv", sep=";", encoding="latin-1")

    provas2014 = [197, 211, 223, 201, 212, 224, 204, 213, 225, 208, 214, 226]
    provas2015 = [232,272, 236, 276, 240, 280, 244, 284]
    provas2016 = [303, 296, 337, 292, 332, 302, 344, 349, 303]
    provas2017 = [393,432,396,436,400,440,406,444]
    provas2018 = [449, 488, 452, 492, 456, 496, 462, 500]
    provas2019 = [512, 552, 508, 548, 505, 544, 518, 556] #DIGG GDIGG DIGG
    provas2020 = [599, 679, 568, 648, 578, 658, 590, 670, 688, 692, 700, 696]
    provas2021 = [911, 991, 880, 960, 890, 970, 902, 982]
    provas2022 = [1087, 1167, 1056, 1136, 1066, 1146, 1078, 1158]

    dItens2014['ANO'] = 2014
    dItens2015['ANO'] = 2015
    dItens2016['ANO'] = 2016
    dItens2017['ANO'] = 2017      
    dItens2018['ANO'] = 2018    
    dItens2019['ANO'] = 2019
    dItens2020['ANO'] = 2020
    dItens2021['ANO'] = 2021
    dItens2022['ANO'] = 2022


    #Colocando as proficiências nas provas e nos dataframes indicados
    dItens2014 = thetaToCsv(provas2014, dItens2014)
    dItens2015 = thetaToCsv(provas2015, dItens2015)
    dItens2016 = thetaToCsv(provas2016, dItens2016)
    dItens2017 = thetaToCsv(provas2017, dItens2017)
    dItens2018 = thetaToCsv(provas2018, dItens2018)
    dItens2019 = thetaToCsv(provas2019, dItens2019)
    dItens2020 = thetaToCsv(provas2020, dItens2020)
    dItens2021 = thetaToCsv(provas2021, dItens2021)
    dItens2022 = thetaToCsv(provas2022, dItens2022)

#    dEnc2017 = pd.read_csv('ITENS_PROVA_2017_ENCCEJA.csv')
#    dEnc2018 = pd.read_csv('ITENS_PROVA_2017_ENCCEJA.csv')
#    dEnc2019 = pd.read_csv('ITENS_PROVA_2017_ENCCEJA.csv')
#    dEnc2020 = pd.read_csv('ITENS_PROVA_2017_ENCCEJA.csv')

    dItens2020 = dItens2020.query("TP_VERSAO_DIGITAL not in [1]")
    del dItens2020['TP_VERSAO_DIGITAL']

    result = pd.concat([dItens2014, dItens2015, dItens2016, dItens2017, dItens2018, dItens2019, dItens2020, dItens2021, dItens2022])
    result['CO_HABILIDADE'].fillna(31, inplace=True)
    result.to_csv('provasOrdernadasPorTri2.csv', index=False, encoding='utf-8', decimal=',')
    result.to_excel("provasOrdernadasPorTri2.xlsx")

    return result

Make()





