import numpy as np
import pandas as pd

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

#Leitura dos dados de 2016 e Escolha da Prova [303 - MT 2 dia]
dItens2016 = pd.read_csv("itens_prova_2016.csv", sep=";", encoding="latin-1")
dItens2018 = pd.read_csv("ITENS_PROVA_2018.csv", sep=";", encoding="latin-1")
dItens2019 = pd.read_csv("ITENS_PROVA_2019.csv", sep=";", encoding="latin-1")
dItens2020 = pd.read_csv("ITENS_PROVA_2020.csv", sep=";", encoding="latin-1")
dItens2021 = pd.read_csv("ITENS_PROVA_2021.csv", sep=";", encoding="latin-1")

provas2016 = [303]
provas2018 = [449, 488, 452, 492, 456, 496, 462, 500]
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